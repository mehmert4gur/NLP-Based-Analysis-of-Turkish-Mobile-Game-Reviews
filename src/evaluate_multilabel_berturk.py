import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    classification_report,
)
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_DIR = Path("outputs/models/berturk_multilabel_absa_full/best_model")
TEST_PATH = Path("data/training/absa_multilabel_test.csv")
LABEL_MAP_PATH = Path("data/training/label_map.json")

OUTPUT_DIR = Path("outputs/reports/berturk_multilabel_absa")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

THRESHOLD = 0.35
MAX_LENGTH = 128
BATCH_SIZE = 16


def load_label_map():
    with open(LABEL_MAP_PATH, "r", encoding="utf-8") as file:
        label_map = json.load(file)

    id_to_label = {
        int(idx): label
        for idx, label in label_map["id_to_label"].items()
    }

    labels = [id_to_label[i] for i in range(len(id_to_label))]
    return labels


def batch_predict(texts, tokenizer, model, device):
    all_probs = []

    for start in range(0, len(texts), BATCH_SIZE):
        batch_texts = texts[start:start + BATCH_SIZE]

        inputs = tokenizer(
            batch_texts,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=MAX_LENGTH,
        )

        inputs = {
            key: value.to(device)
            for key, value in inputs.items()
        }

        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.sigmoid(outputs.logits).cpu().numpy()

        all_probs.append(probs)

    return np.vstack(all_probs)


def main():
    labels = load_label_map()

    df = pd.read_csv(TEST_PATH)
    df["text"] = df["text"].astype(str)

    y_true = df[labels].astype(int).values

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    model.to(device)
    model.eval()

    probs = batch_predict(df["text"].tolist(), tokenizer, model, device)
    y_pred = (probs >= THRESHOLD).astype(int)

    metrics = {
        "threshold": THRESHOLD,
        "micro_f1": f1_score(y_true, y_pred, average="micro", zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "micro_precision": precision_score(y_true, y_pred, average="micro", zero_division=0),
        "micro_recall": recall_score(y_true, y_pred, average="micro", zero_division=0),
        "macro_precision": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "macro_recall": recall_score(y_true, y_pred, average="macro", zero_division=0),
    }

    print("\nOverall metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value}")

    with open(OUTPUT_DIR / "overall_metrics.json", "w", encoding="utf-8") as file:
        json.dump(metrics, file, ensure_ascii=False, indent=2)

    report_dict = classification_report(
        y_true,
        y_pred,
        target_names=labels,
        zero_division=0,
        output_dict=True,
    )

    report_df = pd.DataFrame(report_dict).transpose()
    report_df.to_csv(
        OUTPUT_DIR / "per_label_classification_report.csv",
        encoding="utf-8-sig",
    )

    prob_df = pd.DataFrame(probs, columns=[f"prob_{label}" for label in labels])
    pred_df = pd.DataFrame(y_pred, columns=[f"pred_{label}" for label in labels])

    output_df = pd.concat(
        [
            df.reset_index(drop=True),
            prob_df,
            pred_df,
        ],
        axis=1,
    )

    output_df.to_csv(
        OUTPUT_DIR / "test_predictions.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("\nKaydedilen dosyalar:")
    print(OUTPUT_DIR / "overall_metrics.json")
    print(OUTPUT_DIR / "per_label_classification_report.csv")
    print(OUTPUT_DIR / "test_predictions.csv")


if __name__ == "__main__":
    main()