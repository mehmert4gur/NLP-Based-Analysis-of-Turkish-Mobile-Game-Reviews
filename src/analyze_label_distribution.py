from pathlib import Path

import pandas as pd


TRAIN_PATH = Path("data/training/absa_multilabel_train.csv")
VAL_PATH = Path("data/training/absa_multilabel_val.csv")
TEST_PATH = Path("data/training/absa_multilabel_test.csv")
ALL_PATH = Path("data/training/absa_multilabel_all.csv")

OUTPUT_PATH = Path("outputs/reports/label_distribution.csv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


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
    return [
        column
        for column in df.columns
        if column not in NON_LABEL_COLUMNS
    ]


def summarize_split(name, path):
    df = pd.read_csv(path)
    label_columns = get_label_columns(df)

    total_rows = len(df)
    rows = []

    for label in label_columns:
        count = int(df[label].sum())
        ratio = count / total_rows if total_rows else 0

        rows.append({
            "split": name,
            "label": label,
            "count": count,
            "ratio": round(ratio, 4),
        })

    return pd.DataFrame(rows)


def main():
    all_dist = summarize_split("all", ALL_PATH)
    train_dist = summarize_split("train", TRAIN_PATH)
    val_dist = summarize_split("val", VAL_PATH)
    test_dist = summarize_split("test", TEST_PATH)

    result = pd.concat(
        [all_dist, train_dist, val_dist, test_dist],
        ignore_index=True
    )

    result.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("\nLabel distribution kaydedildi:")
    print(OUTPUT_PATH)

    print("\nALL split - en sık 10 label:")
    print(
        all_dist.sort_values("count", ascending=False)
        .head(10)
        .to_string(index=False)
    )

    print("\nALL split - en nadir 10 label:")
    print(
        all_dist.sort_values("count", ascending=True)
        .head(10)
        .to_string(index=False)
    )

    max_count = all_dist["count"].max()
    min_count = all_dist["count"].min()

    print("\nImbalance summary:")
    print(f"Max label count: {max_count}")
    print(f"Min label count: {min_count}")
    print(f"Imbalance ratio: {round(max_count / min_count, 2) if min_count else 'inf'}")


if __name__ == "__main__":
    main()