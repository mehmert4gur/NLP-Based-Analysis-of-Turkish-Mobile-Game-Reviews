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
LABEL_MAP_PATH = Path("data/training/label_map.json")

OUTPUT_DIR = Path("outputs/models/berturk_multilabel_absa_pilot")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_LENGTH = 96
THRESHOLD = 0.5

PILOT_TRAIN_SIZE = 1000
PILOT_VAL_SIZE = 300


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


def load_dataset(path, labels, max_rows=None):
    df = pd.read_csv(path)
    df["text"] = df["text"].astype(str)

    if max_rows is not None:
        df = df.sample(
            n=min(max_rows, len(df)),
            random_state=42
        ).reset_index(drop=True)

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
    }


def main():
    labels, label_to_id, id_to_label = load_label_map()
    num_labels = len(labels)

    print(f"Pilot eğitim başlıyor.")
    print(f"Label sayısı: {num_labels}")
    print(f"Train örnek sayısı: {PILOT_TRAIN_SIZE}")
    print(f"Val örnek sayısı: {PILOT_VAL_SIZE}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    train_dataset = load_dataset(TRAIN_PATH, labels, PILOT_TRAIN_SIZE)
    val_dataset = load_dataset(VAL_PATH, labels, PILOT_VAL_SIZE)

    def tokenize_batch(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            padding="max_length",
            max_length=MAX_LENGTH,
        )

    train_dataset = train_dataset.map(tokenize_batch, batched=True)
    val_dataset = val_dataset.map(tokenize_batch, batched=True)

    train_dataset.set_format(
        type="torch",
        columns=["input_ids", "attention_mask", "labels"],
    )

    val_dataset.set_format(
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
        save_strategy="no",
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=1,
        weight_decay=0.01,
        logging_steps=20,
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )

    trainer.train()

    print("\nPilot validation sonucu:")
    metrics = trainer.evaluate(val_dataset)
    print(metrics)

    trainer.save_model(str(OUTPUT_DIR / "pilot_model"))
    tokenizer.save_pretrained(str(OUTPUT_DIR / "pilot_model"))

    print(f"\nPilot model kaydedildi: {OUTPUT_DIR / 'pilot_model'}")


if __name__ == "__main__":
    main()