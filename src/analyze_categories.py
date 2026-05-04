import pandas as pd
import re
import unicodedata
from pathlib import Path

from category_rules import CATEGORY_KEYWORDS

INPUT_PATH = Path("data/processed/temiz_yorumlar.xlsx")
OUTPUT_PATH = Path("data/processed/kategori_analizi.xlsx")


def normalize_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()

    replacements = {
        "ı": "i",
        "ğ": "g",
        "ü": "u",
        "ş": "s",
        "ö": "o",
        "ç": "c",
        "İ": "i",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def find_categories(text):
    found_categories = []

    normalized_text = normalize_text(text)

    if normalized_text == "":
        return found_categories

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            normalized_keyword = normalize_text(keyword)

            if normalized_keyword in normalized_text:
                found_categories.append(category)
                break

    return found_categories


def analyze():
    df = pd.read_excel(INPUT_PATH)

    print("Toplam yorum:", len(df))

    if "is_analyzable" not in df.columns:
        raise ValueError(
            "temiz_yorumlar.xlsx içinde 'is_analyzable' sütunu yok. "
            "Önce py src/preprocess_reviews.py çalıştır."
        )

    df["categories"] = [[] for _ in range(len(df))]

    analyzable_mask = df["is_analyzable"] == True

    df.loc[analyzable_mask, "categories"] = (
        df.loc[analyzable_mask, "clean_text"].apply(find_categories)
    )

    df["category_count"] = df["categories"].apply(len)
    df["has_category"] = df["category_count"] > 0

    df.to_excel(OUTPUT_PATH, index=False)

    print("Analize uygun yorum:", analyzable_mask.sum())
    print("Kategori bulunan yorum:", df["has_category"].sum())
    print("Kategori bulunamayan yorum:", (~df["has_category"] & analyzable_mask).sum())
    print("Analize uygun olmayan yorum:", (~analyzable_mask).sum())

    print("\nKategori dağılımı:")
    exploded = df.explode("categories")
    print(exploded["categories"].value_counts())

    print("\nKaydedildi:", OUTPUT_PATH)


if __name__ == "__main__":
    analyze()