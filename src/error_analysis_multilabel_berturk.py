from pathlib import Path

import pandas as pd


PREDICTIONS_PATH = Path("outputs/reports/berturk_multilabel_absa/test_predictions.csv")
OUTPUT_DIR = Path("outputs/error_analysis/berturk_multilabel_absa")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_EXAMPLES_PER_LABEL = 50


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


def main():
    df = pd.read_csv(PREDICTIONS_PATH)
    labels = get_label_columns(df)

    fp_rows = []
    fn_rows = []

    for label in labels:
        pred_col = f"pred_{label}"
        prob_col = f"prob_{label}"

        if pred_col not in df.columns or prob_col not in df.columns:
            continue

        false_positive = df[
            (df[label] == 0) &
            (df[pred_col] == 1)
        ].copy()

        false_negative = df[
            (df[label] == 1) &
            (df[pred_col] == 0)
        ].copy()

        false_positive = false_positive.sort_values(
            prob_col,
            ascending=False
        ).head(MAX_EXAMPLES_PER_LABEL)

        false_negative = false_negative.sort_values(
            prob_col,
            ascending=False
        ).head(MAX_EXAMPLES_PER_LABEL)

        for _, row in false_positive.iterrows():
            fp_rows.append({
                "label": label,
                "error_type": "false_positive",
                "probability": row.get(prob_col, ""),
                "text": row.get("text", ""),
                "true_labels": row.get("labels", ""),
                "content": row.get("content", ""),
                "score": row.get("score", ""),
                "general_sentiment": row.get("general_sentiment", ""),
            })

        for _, row in false_negative.iterrows():
            fn_rows.append({
                "label": label,
                "error_type": "false_negative",
                "probability": row.get(prob_col, ""),
                "text": row.get("text", ""),
                "true_labels": row.get("labels", ""),
                "content": row.get("content", ""),
                "score": row.get("score", ""),
                "general_sentiment": row.get("general_sentiment", ""),
            })

    fp_df = pd.DataFrame(fp_rows)
    fn_df = pd.DataFrame(fn_rows)

    fp_df.to_excel(OUTPUT_DIR / "false_positives.xlsx", index=False)
    fn_df.to_excel(OUTPUT_DIR / "false_negatives.xlsx", index=False)

    summary_rows = []

    for label in labels:
        pred_col = f"pred_{label}"

        if pred_col not in df.columns:
            continue

        tp = int(((df[label] == 1) & (df[pred_col] == 1)).sum())
        fp = int(((df[label] == 0) & (df[pred_col] == 1)).sum())
        fn = int(((df[label] == 1) & (df[pred_col] == 0)).sum())
        tn = int(((df[label] == 0) & (df[pred_col] == 0)).sum())

        summary_rows.append({
            "label": label,
            "true_positive": tp,
            "false_positive": fp,
            "false_negative": fn,
            "true_negative": tn,
        })

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(
        OUTPUT_DIR / "error_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("Error analysis kaydedildi:")
    print(OUTPUT_DIR / "false_positives.xlsx")
    print(OUTPUT_DIR / "false_negatives.xlsx")
    print(OUTPUT_DIR / "error_summary.csv")


if __name__ == "__main__":
    main()