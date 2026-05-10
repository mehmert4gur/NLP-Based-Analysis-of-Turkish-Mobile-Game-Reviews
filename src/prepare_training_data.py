# src/prepare_training_data.py

import ast
import json
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


INPUT_PATH = Path("data/processed/kategori_analizi.xlsx")
OUTPUT_DIR = Path("data/training")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MULTILABEL_ALL_PATH = OUTPUT_DIR / "absa_multilabel_all.csv"
MULTILABEL_TRAIN_PATH = OUTPUT_DIR / "absa_multilabel_train.csv"
MULTILABEL_VAL_PATH = OUTPUT_DIR / "absa_multilabel_val.csv"
MULTILABEL_TEST_PATH = OUTPUT_DIR / "absa_multilabel_test.csv"

SENTIMENT_ALL_PATH = OUTPUT_DIR / "sentiment_all.csv"
SENTIMENT_TRAIN_PATH = OUTPUT_DIR / "sentiment_train.csv"
SENTIMENT_VAL_PATH = OUTPUT_DIR / "sentiment_val.csv"
SENTIMENT_TEST_PATH = OUTPUT_DIR / "sentiment_test.csv"

LABEL_MAP_PATH = OUTPUT_DIR / "label_map.json"
SENTIMENT_LABEL_MAP_PATH = OUTPUT_DIR / "sentiment_label_map.json"

RANDOM_STATE = 42
MIN_CATEGORY_FREQUENCY = 5
MAX_CATEGORY_COUNT_FOR_TRAINING = 4


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


def normalize_bool(value):
    if isinstance(value, bool):
        return value

    if pd.isna(value):
        return False

    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "evet"}

    return bool(value)


def normalize_text_column(df):
    if "clean_text" not in df.columns:
        raise ValueError("Input dosyasında 'clean_text' kolonu bulunamadı.")

    df["text"] = df["clean_text"].astype(str).str.strip()
    df = df[df["text"] != ""].copy()

    return df


def apply_training_quality_filters(df):
    df = df.copy()

    if "categories" in df.columns:
        df["categories"] = df["categories"].apply(safe_parse_list)

    if "category_count" not in df.columns and "categories" in df.columns:
        df["category_count"] = df["categories"].apply(len)

    before = len(df)

    if "rating_text_contradiction" in df.columns:
        df["rating_text_contradiction"] = df["rating_text_contradiction"].apply(
            normalize_bool
        )
        df = df[df["rating_text_contradiction"] == False].copy()

    if "category_count" in df.columns:
        df = df[df["category_count"] > 0].copy()
        df = df[df["category_count"] <= MAX_CATEGORY_COUNT_FOR_TRAINING].copy()

    after = len(df)

    print(f"Quality filter öncesi: {before}")
    print(f"Quality filter sonrası: {after}")
    print(f"Çıkarılan satır: {before - after}")

    return df


def prepare_multilabel_dataset(df):
    if "categories" not in df.columns:
        raise ValueError("Input dosyasında 'categories' kolonu bulunamadı.")

    df = df.copy()
    df["categories"] = df["categories"].apply(safe_parse_list)
    df = df[df["categories"].apply(len) > 0].copy()

    category_counts = (
        df.explode("categories")["categories"]
        .value_counts()
        .to_dict()
    )

    allowed_categories = sorted([
        category
        for category, count in category_counts.items()
        if count >= MIN_CATEGORY_FREQUENCY
    ])

    if not allowed_categories:
        raise ValueError("Yeterli frekansta kategori bulunamadı.")

    label_to_id = {
        label: idx
        for idx, label in enumerate(allowed_categories)
    }

    def filter_categories(categories):
        return [
            category
            for category in categories
            if category in label_to_id
        ]

    df["labels"] = df["categories"].apply(filter_categories)
    df = df[df["labels"].apply(len) > 0].copy()

    for label in allowed_categories:
        df[label] = df["labels"].apply(lambda labels: 1 if label in labels else 0)

    output_columns = [
        "text",
        "labels",
        *allowed_categories,
    ]

    optional_columns = [
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
    ]

    for column in optional_columns:
        if column in df.columns:
            output_columns.append(column)

    multilabel_df = df[output_columns].copy()

    label_map = {
        "label_to_id": label_to_id,
        "id_to_label": {str(idx): label for label, idx in label_to_id.items()},
        "min_category_frequency": MIN_CATEGORY_FREQUENCY,
        "max_category_count_for_training": MAX_CATEGORY_COUNT_FOR_TRAINING,
        "num_labels": len(label_to_id),
    }

    return multilabel_df, label_map


def prepare_sentiment_dataset(df):
    if "general_sentiment" not in df.columns:
        raise ValueError("Input dosyasında 'general_sentiment' kolonu bulunamadı.")

    sentiment_df = df.copy()
    sentiment_df = sentiment_df[
        sentiment_df["general_sentiment"].isin(
            ["negative", "neutral", "positive", "mixed"]
        )
    ].copy()

    label_order = ["negative", "neutral", "positive", "mixed"]
    label_to_id = {
        label: idx
        for idx, label in enumerate(label_order)
    }

    sentiment_df["label"] = sentiment_df["general_sentiment"].map(label_to_id)

    output_columns = ["text", "general_sentiment", "label"]

    optional_columns = [
        "content",
        "score",
        "rating",
        "app_name",
        "review_created_at",
        "sentiment_score",
        "positive_score",
        "negative_score",
        "sentiment_evidence",
        "categories",
        "rating_text_contradiction",
    ]

    for column in optional_columns:
        if column in sentiment_df.columns:
            output_columns.append(column)

    sentiment_df = sentiment_df[output_columns].copy()

    sentiment_label_map = {
        "label_to_id": label_to_id,
        "id_to_label": {str(idx): label for label, idx in label_to_id.items()},
        "num_labels": len(label_to_id),
    }

    return sentiment_df, sentiment_label_map


def split_dataset(df, stratify_column=None):
    stratify_values = None

    if stratify_column and stratify_column in df.columns:
        value_counts = df[stratify_column].value_counts()
        if value_counts.min() >= 2:
            stratify_values = df[stratify_column]

    train_df, temp_df = train_test_split(
        df,
        test_size=0.30,
        random_state=RANDOM_STATE,
        shuffle=True,
        stratify=stratify_values,
    )

    temp_stratify_values = None

    if stratify_column and stratify_column in temp_df.columns:
        value_counts = temp_df[stratify_column].value_counts()
        if value_counts.min() >= 2:
            temp_stratify_values = temp_df[stratify_column]

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        random_state=RANDOM_STATE,
        shuffle=True,
        stratify=temp_stratify_values,
    )

    return train_df, val_df, test_df


def save_dataset(df, path):
    df.to_csv(path, index=False, encoding="utf-8-sig")


def main():
    df = pd.read_excel(INPUT_PATH)
    df = normalize_text_column(df)
    df = apply_training_quality_filters(df)

    print(f"Training için kalan input rows: {len(df)}")

    multilabel_df, label_map = prepare_multilabel_dataset(df)
    save_dataset(multilabel_df, MULTILABEL_ALL_PATH)

    train_df, val_df, test_df = split_dataset(multilabel_df)
    save_dataset(train_df, MULTILABEL_TRAIN_PATH)
    save_dataset(val_df, MULTILABEL_VAL_PATH)
    save_dataset(test_df, MULTILABEL_TEST_PATH)

    with open(LABEL_MAP_PATH, "w", encoding="utf-8") as file:
        json.dump(label_map, file, ensure_ascii=False, indent=2)

    sentiment_df, sentiment_label_map = prepare_sentiment_dataset(df)
    save_dataset(sentiment_df, SENTIMENT_ALL_PATH)

    sentiment_train_df, sentiment_val_df, sentiment_test_df = split_dataset(
        sentiment_df,
        stratify_column="general_sentiment",
    )

    save_dataset(sentiment_train_df, SENTIMENT_TRAIN_PATH)
    save_dataset(sentiment_val_df, SENTIMENT_VAL_PATH)
    save_dataset(sentiment_test_df, SENTIMENT_TEST_PATH)

    with open(SENTIMENT_LABEL_MAP_PATH, "w", encoding="utf-8") as file:
        json.dump(sentiment_label_map, file, ensure_ascii=False, indent=2)

    print("\nMultilabel ABSA dataset")
    print(f"All:   {len(multilabel_df)} -> {MULTILABEL_ALL_PATH}")
    print(f"Train: {len(train_df)} -> {MULTILABEL_TRAIN_PATH}")
    print(f"Val:   {len(val_df)} -> {MULTILABEL_VAL_PATH}")
    print(f"Test:  {len(test_df)} -> {MULTILABEL_TEST_PATH}")
    print(f"Labels: {label_map['num_labels']} -> {LABEL_MAP_PATH}")

    print("\nSentiment dataset")
    print(f"All:   {len(sentiment_df)} -> {SENTIMENT_ALL_PATH}")
    print(f"Train: {len(sentiment_train_df)} -> {SENTIMENT_TRAIN_PATH}")
    print(f"Val:   {len(sentiment_val_df)} -> {SENTIMENT_VAL_PATH}")
    print(f"Test:  {len(sentiment_test_df)} -> {SENTIMENT_TEST_PATH}")
    print(f"Labels: {sentiment_label_map['num_labels']} -> {SENTIMENT_LABEL_MAP_PATH}")


if __name__ == "__main__":
    main()