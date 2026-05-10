from pathlib import Path

import ast
import pandas as pd


PREDICTIONS_PATH = Path("outputs/reports/berturk_multilabel_absa/test_predictions.csv")
OUTPUT_DIR = Path("outputs/reports/berturk_multilabel_absa")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SUMMARY_PATH = OUTPUT_DIR / "rule_vs_berturk_summary.csv"
DISAGREEMENTS_PATH = OUTPUT_DIR / "rule_vs_berturk_disagreements.xlsx"
BERT_ONLY_PATH = OUTPUT_DIR / "berturk_only_predictions.xlsx"
RULE_ONLY_PATH = OUTPUT_DIR / "rule_only_predictions.xlsx"

PROB_THRESHOLD_FOR_REVIEW = 0.35


NON_LABEL_COLUMNS = {
    "text",
    "labels",
    "content",
    "score",
    "rating",
    "app_name",
    "review_created_at",
    "general_sentiment",
    "sentiment_score",
    "category_count",
    "match_details",
    "local_aspect_sentiments",
    "rating_text_contradiction",
}


def safe_parse_list(value):
    if isinstance(value, list):
        return value

    if pd.isna(value):
        return []

    if isinstance(value, str):
        value = value.strip()

        if not value:
            return []

        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            return []

    return []


def get_label_columns(df):
    labels = []

    for column in df.columns:
        if column in NON_LABEL_COLUMNS:
            continue

        if column.startswith("prob_"):
            continue

        if column.startswith("pred_"):
            continue

        if pd.api.types.is_numeric_dtype(df[column]):
            unique_values = set(df[column].dropna().unique())
            if unique_values.issubset({0, 1}):
                labels.append(column)

    return labels


def labels_from_binary_row(row, labels, prefix=""):
    found = []

    for label in labels:
        column = f"{prefix}{label}" if prefix else label

        if column in row.index and row[column] == 1:
            found.append(label)

    return found


def main():
    df = pd.read_csv(PREDICTIONS_PATH)
    labels = get_label_columns(df)

    rows = []
    disagreement_rows = []
    bert_only_rows = []
    rule_only_rows = []

    for _, row in df.iterrows():
        rule_labels = set(labels_from_binary_row(row, labels))
        bert_labels = set(labels_from_binary_row(row, labels, prefix="pred_"))

        intersection = rule_labels & bert_labels
        union = rule_labels | bert_labels

        bert_only = sorted(bert_labels - rule_labels)
        rule_only = sorted(rule_labels - bert_labels)

        jaccard = len(intersection) / len(union) if union else 1.0

        rows.append({
            "text": row.get("text", ""),
            "rule_labels": sorted(rule_labels),
            "bert_labels": sorted(bert_labels),
            "common_labels": sorted(intersection),
            "bert_only": bert_only,
            "rule_only": rule_only,
            "rule_count": len(rule_labels),
            "bert_count": len(bert_labels),
            "common_count": len(intersection),
            "jaccard": round(jaccard, 4),
            "content": row.get("content", ""),
            "score": row.get("score", ""),
            "general_sentiment": row.get("general_sentiment", ""),
        })

        if bert_only or rule_only:
            disagreement_rows.append({
                "text": row.get("text", ""),
                "rule_labels": sorted(rule_labels),
                "bert_labels": sorted(bert_labels),
                "bert_only": bert_only,
                "rule_only": rule_only,
                "jaccard": round(jaccard, 4),
                "content": row.get("content", ""),
                "score": row.get("score", ""),
                "general_sentiment": row.get("general_sentiment", ""),
            })

        for label in bert_only:
            prob_col = f"prob_{label}"

            bert_only_rows.append({
                "label": label,
                "probability": row.get(prob_col, ""),
                "text": row.get("text", ""),
                "rule_labels": sorted(rule_labels),
                "bert_labels": sorted(bert_labels),
                "content": row.get("content", ""),
                "score": row.get("score", ""),
                "general_sentiment": row.get("general_sentiment", ""),
            })

        for label in rule_only:
            prob_col = f"prob_{label}"

            rule_only_rows.append({
                "label": label,
                "probability": row.get(prob_col, ""),
                "text": row.get("text", ""),
                "rule_labels": sorted(rule_labels),
                "bert_labels": sorted(bert_labels),
                "content": row.get("content", ""),
                "score": row.get("score", ""),
                "general_sentiment": row.get("general_sentiment", ""),
            })

    comparison_df = pd.DataFrame(rows)

    summary = {
        "total_rows": len(comparison_df),
        "average_jaccard": comparison_df["jaccard"].mean(),
        "exact_match_count": int((comparison_df["jaccard"] == 1.0).sum()),
        "disagreement_count": len(disagreement_rows),
        "bert_only_prediction_count": len(bert_only_rows),
        "rule_only_prediction_count": len(rule_only_rows),
    }

    summary_df = pd.DataFrame([summary])
    summary_df.to_csv(SUMMARY_PATH, index=False, encoding="utf-8-sig")

    pd.DataFrame(disagreement_rows).to_excel(DISAGREEMENTS_PATH, index=False)
    pd.DataFrame(bert_only_rows).to_excel(BERT_ONLY_PATH, index=False)
    pd.DataFrame(rule_only_rows).to_excel(RULE_ONLY_PATH, index=False)

    print("Rule vs BERTürk karşılaştırması tamamlandı.")
    print("\nSummary:")
    print(summary)

    print("\nKaydedilen dosyalar:")
    print(SUMMARY_PATH)
    print(DISAGREEMENTS_PATH)
    print(BERT_ONLY_PATH)
    print(RULE_ONLY_PATH)


if __name__ == "__main__":
    main()