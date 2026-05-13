import json
from pathlib import Path

import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from datasets import Dataset
from sklearn.metrics import f1_score, precision_score, recall_score, classification_report
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)


MODEL_NAME = "dbmdz/bert-base-turkish-cased"

TRAIN_PATH = Path("data/training/absa_multilabel_train.csv")
VAL_PATH = Path("data/training/absa_multilabel_val.csv")
TEST_PATH = Path("data/training/absa_multilabel_test.csv")
LABEL_MAP_PATH = Path("data/training/label_map.json")

OUTPUT_DIR = Path("outputs/models/berturk_multilabel_absa_full")
BEST_MODEL_DIR = OUTPUT_DIR / "best_model"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_LENGTH = 128


def load_label_map():
    with open(LABEL_MAP_PATH, "r", encoding="utf-8") as file:
        label_map = json.load(file)

    id_to_label = {
        int(idx): label
        for idx, label in label_map["id_to_label"].items()
    }

    label_to_id = label_map["label_to_id"]
    labels = [id_to_label[i] for i in range(len(id_to_label))]

    return labels, label_to_id, id_to_label


def load_dataset(path, labels):
    df = pd.read_csv(path)
    df["text"] = df["text"].astype(str)

    label_matrix = df[labels].astype(float).values.tolist()
    df["labels"] = label_matrix

    return Dataset.from_pandas(df[["text", "labels"]])


def calculate_pos_weights(dataset, num_labels):
    """Sınıf dengesizliğini çözmek için class weight (pos_weight) hesaplar."""
    all_labels = torch.tensor(dataset["labels"])
    pos_counts = all_labels.sum(dim=0)
    neg_counts = all_labels.shape[0] - pos_counts
    
    # Sıfıra bölmeyi engelle
    pos_counts = torch.clamp(pos_counts, min=1.0)
    
    pos_weights = neg_counts / pos_counts
    # Aşırı büyük ağırlıkları sınırla
    pos_weights = torch.clamp(pos_weights, max=10.0)
    
    return pos_weights


def find_optimal_thresholds(y_true, logits):
    """Validation seti üzerinde 0.10 ile 0.90 arasında arama yaparak her sınıf için optimum eşiği bulur."""
    probabilities = 1 / (1 + np.exp(-logits))
    num_classes = y_true.shape[1]
    best_thresholds = np.full(num_classes, 0.35)
    
    thresholds_to_try = np.arange(0.10, 0.91, 0.05)
    
    for class_idx in range(num_classes):
        best_f1 = -1
        best_th = 0.35
        for th in thresholds_to_try:
            preds = (probabilities[:, class_idx] >= th).astype(int)
            f1 = f1_score(y_true[:, class_idx], preds, zero_division=0)
            if f1 > best_f1:
                best_f1 = f1
                best_th = th
        best_thresholds[class_idx] = best_th
        
    return best_thresholds


class MetricComputer:
    def __init__(self, labels_list, optimize_thresholds=True, thresholds=None):
        self.labels_list = labels_list
        self.optimize_thresholds = optimize_thresholds
        if thresholds is None:
            self.thresholds = np.full(len(labels_list), 0.35)
        else:
            self.thresholds = thresholds
            
    def __call__(self, eval_pred):
        logits, labels = eval_pred
        
        if self.optimize_thresholds:
            self.thresholds = find_optimal_thresholds(labels, logits)
            
        probabilities = 1 / (1 + np.exp(-logits))
        predictions = (probabilities >= self.thresholds).astype(int)
        
        metrics = {
            "micro_f1": f1_score(labels, predictions, average="micro", zero_division=0),
            "macro_f1": f1_score(labels, predictions, average="macro", zero_division=0),
            "micro_precision": precision_score(labels, predictions, average="micro", zero_division=0),
            "micro_recall": recall_score(labels, predictions, average="micro", zero_division=0),
            "macro_precision": precision_score(labels, predictions, average="macro", zero_division=0),
            "macro_recall": recall_score(labels, predictions, average="macro", zero_division=0),
        }
        
        report = classification_report(labels, predictions, target_names=self.labels_list, output_dict=True, zero_division=0)
        
        print("\n" + "="*75)
        print(f"PER-CLASS METRICS {'(OPTIMIZED)' if self.optimize_thresholds else '(FIXED THRESHOLDS)'}")
        print("="*75)
        print(f"{'Kategori':<30} | {'Thresh':<6} | {'F1':<6} | {'Prec':<6} | {'Rec':<6} | {'Support':<6}")
        print("-" * 75)
        for i, label_name in enumerate(self.labels_list):
            if label_name in report:
                stats = report[label_name]
                th = self.thresholds[i]
                support = stats['support']
                
                # Düşük support için belirteç ekleyelim
                marker = "*" if support < 50 else " "
                
                print(f"{label_name[:28]:<28}{marker} | {th:.2f}   | {stats['f1-score']:.4f} | {stats['precision']:.4f} | {stats['recall']:.4f} | {support:<6.0f}")
        print("*" * 75)
        print("(*) Düşük support (<50)\n")
        
        return metrics


class CustomTrainer(Trainer):
    def __init__(self, pos_weights=None, **kwargs):
        super().__init__(**kwargs)
        if pos_weights is not None:
            self.pos_weights = pos_weights.clone().detach()
        else:
            self.pos_weights = None

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits
        
        if self.pos_weights is not None:
            pos_weights = self.pos_weights.to(logits.device)
            loss_fct = nn.BCEWithLogitsLoss(pos_weight=pos_weights)
        else:
            loss_fct = nn.BCEWithLogitsLoss()
            
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), 
                        labels.float().view(-1, self.model.config.num_labels))
        
        return (loss, outputs) if return_outputs else loss


def main():
    labels, label_to_id, id_to_label = load_label_map()
    num_labels = len(labels)

    print(f"Full BERTürk multi-label ABSA eğitimi başlıyor.")
    print(f"Label sayısı: {num_labels}")
    print(labels)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    train_dataset = load_dataset(TRAIN_PATH, labels)
    val_dataset = load_dataset(VAL_PATH, labels)
    test_dataset = load_dataset(TEST_PATH, labels)

    # Class weight hesaplama
    pos_weights = calculate_pos_weights(train_dataset, num_labels)
    print(f"\nHesaplanan Class Ağırlıkları (pos_weights):")
    for i, label in enumerate(labels):
        print(f"  {label:<30}: {pos_weights[i]:.2f}")

    def tokenize_batch(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            padding="max_length",
            max_length=MAX_LENGTH,
        )

    train_dataset = train_dataset.map(tokenize_batch, batched=True)
    val_dataset = val_dataset.map(tokenize_batch, batched=True)
    test_dataset = test_dataset.map(tokenize_batch, batched=True)

    train_dataset.set_format(
        type="torch",
        columns=["input_ids", "attention_mask", "labels"],
    )

    val_dataset.set_format(
        type="torch",
        columns=["input_ids", "attention_mask", "labels"],
    )

    test_dataset.set_format(
        type="torch",
        columns=["input_ids", "attention_mask", "labels"],
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=num_labels,
        problem_type="multi_label_classification",
        id2label=id_to_label,
        label2id=label_to_id,
    )

    # Training stabilization: warmup_ratio=0.1 eklendi
    training_args = TrainingArguments(
        output_dir=str(OUTPUT_DIR),
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=4,
        weight_decay=0.01,
        warmup_ratio=0.1,  # Eklendi
        logging_steps=50,
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        save_total_limit=2,
        report_to="none",
        fp16=True,
    )

    # Epoch değerlendirmelerinde threshold optimizasyonu yap
    metric_computer = MetricComputer(labels, optimize_thresholds=True)

    trainer = CustomTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=metric_computer,
        pos_weights=pos_weights,  # Eklendi
    )

    trainer.train()

    print("\n" + "="*50)
    print("Eğitim Tamamlandı. En İyi Model ile Sonuçlar Üretiliyor...")
    print("="*50)

    # En iyi model ile threshold'ları kalıcı hale getir
    print("\nValidation seti üzerinden nihai eşikler (thresholds) hesaplanıyor...")
    val_predictions = trainer.predict(val_dataset)
    best_thresholds = find_optimal_thresholds(val_predictions.label_ids, val_predictions.predictions)
    
    threshold_dict = {id_to_label[i]: float(best_thresholds[i]) for i in range(num_labels)}
    with open(OUTPUT_DIR / "class_thresholds.json", "w", encoding="utf-8") as file:
        json.dump(threshold_dict, file, ensure_ascii=False, indent=2)
    print("Sınıf bazlı optimum eşikler 'class_thresholds.json' olarak kaydedildi.")

    print("\nValidation sonucu:")
    # Test ve final eval için threshold tuning kapatılıp bulunan eşikler verilir
    trainer.compute_metrics = MetricComputer(labels, optimize_thresholds=False, thresholds=best_thresholds)
    val_metrics = trainer.evaluate(val_dataset)
    print(val_metrics)

    print("\nTest sonucu:")
    test_metrics = trainer.evaluate(test_dataset)
    print(test_metrics)

    trainer.save_model(str(BEST_MODEL_DIR))
    tokenizer.save_pretrained(str(BEST_MODEL_DIR))

    with open(OUTPUT_DIR / "val_metrics.json", "w", encoding="utf-8") as file:
        json.dump(val_metrics, file, ensure_ascii=False, indent=2)

    with open(OUTPUT_DIR / "test_metrics.json", "w", encoding="utf-8") as file:
        json.dump(test_metrics, file, ensure_ascii=False, indent=2)

    print(f"\nBest model ve eşikler kaydedildi: {BEST_MODEL_DIR}")


if __name__ == "__main__":
    main()