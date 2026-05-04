import pandas as pd
import re
from pathlib import Path

RAW_PATH = Path("data/raw/yerel_oyun_yorumlari.xlsx")
PROCESSED_PATH = Path("data/processed/temiz_yorumlar.xlsx")

PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)


def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-zA-ZğüşöçıİĞÜŞÖÇ0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def preprocess():
    df = pd.read_excel(RAW_PATH)

    print("İlk veri boyutu:", len(df))

    df = df.dropna(subset=["content"])
    df = df[df["content"].astype(str).str.strip() != ""]
    df = df.drop_duplicates(subset=["review_id"])

    df["clean_text"] = df["content"].apply(clean_text)

    df["is_empty_after_cleaning"] = df["clean_text"].str.strip() == ""
    df["word_count"] = df["clean_text"].apply(lambda x: len(str(x).split()))
    df["is_short"] = df["word_count"] < 3

    df["is_analyzable"] = (
        (df["is_empty_after_cleaning"] == False) &
        (df["word_count"] >= 2)
    )

    df["review_created_at"] = pd.to_datetime(df["review_created_at"], errors="coerce")
    df["year"] = df["review_created_at"].dt.year
    df["month"] = df["review_created_at"].dt.month

    df.to_excel(PROCESSED_PATH, index=False)

    print("Temizlik sonrası toplam:", len(df))
    print("Temizleme sonrası boş kalan:", df["is_empty_after_cleaning"].sum())
    print("Çok kısa yorum:", df["is_short"].sum())
    print("Analize uygun yorum:", df["is_analyzable"].sum())
    print("Kaydedildi:", PROCESSED_PATH)


if __name__ == "__main__":
    preprocess()