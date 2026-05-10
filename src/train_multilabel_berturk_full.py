import json
from pathlib import Path

import numpy as np
import pandas as pd
from datasets import Dataset
from sklearn.metrics import f1_score, precision_score, recall_score
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
THRESHOLD = 0.35


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


def compute_metrics(eval_pred):
    logits, labels = eval_pred

    probabilities = 1 / (1 + np.exp(-logits))
    predictions = (probabilities >= THRESHOLD).astype(int)

    return {
        "micro_f1": f1_score(labels, predictions, average="micro", zero_division=0),
        "macro_f1": f1_score(labels, predictions, average="macro", zero_division=0),
        "micro_precision": precision_score(labels, predictions, average="micro", zero_division=0),
        "micro_recall": recall_score(labels, predictions, average="micro", zero_division=0),
        "macro_precision": precision_score(labels, predictions, average="macro", zero_division=0),
        "macro_recall": recall_score(labels, predictions, average="macro", zero_division=0),
    }


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

    training_args = TrainingArguments(
        output_dir=str(OUTPUT_DIR),
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=4,
        weight_decay=0.01,
        logging_steps=50,
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        save_total_limit=2,
        report_to="none",
        fp16=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )

    trainer.train()

    print("\nValidation sonucu:")
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

    print(f"\nBest model kaydedildi: {BEST_MODEL_DIR}")


if __name__ == "__main__":
    main()