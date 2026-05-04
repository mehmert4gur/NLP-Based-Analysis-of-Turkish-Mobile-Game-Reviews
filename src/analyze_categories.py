# src/analyze_categories.py

import pandas as pd
import re
from pathlib import Path
from rapidfuzz import fuzz

from category_rules import CATEGORY_RULES

INPUT_PATH = Path("data/processed/temiz_yorumlar.xlsx")
OUTPUT_PATH = Path("data/processed/kategori_analizi.xlsx")


def exact_match(text, keywords):
    return any(keyword in text for keyword in keywords)


def regex_match(text, patterns):
    return any(re.search(pattern, text) for pattern in patterns)


def fuzzy_match(text, fuzzy_terms, threshold=88):
    words = text.split()

    for term in fuzzy_terms:
        if len(term) <= 3:
            continue

        for word in words:
            if len(word) <= 3:
                continue

            if fuzz.ratio(word, term) >= threshold:
                return True

    return False


def find_categories(text):
    if not isinstance(text, str) or not text.strip():
        return []

    found_categories = []

    for category, rules in CATEGORY_RULES.items():
        keywords = rules.get("keywords", [])
        regex_patterns = rules.get("regex", [])
        fuzzy_terms = rules.get("fuzzy", [])

        if exact_match(text, keywords):
            found_categories.append(category)
            continue

        if regex_match(text, regex_patterns):
            found_categories.append(category)
            continue

        if fuzzy_match(text, fuzzy_terms):
            found_categories.append(category)
            continue

    return found_categories


def analyze():
    df = pd.read_excel(INPUT_PATH)

    print("Toplam yorum:", len(df))

    if "is_analyzable" not in df.columns:
        raise ValueError(
            "temiz_yorumlar.xlsx içinde 'is_analyzable' sütunu yok. "
            "Önce python src/preprocess_reviews.py çalıştır."
        )

    # Sadece analize uygun yorumları al
    df = df[df["is_analyzable"] == True].copy()

    print("Analize alınan yorum:", len(df))

    df["categories"] = df["clean_text"].apply(find_categories)
    df["category_count"] = df["categories"].apply(len)
    df["has_category"] = df["category_count"] > 0

    df.to_excel(OUTPUT_PATH, index=False)

    print("Kategori bulunan yorum:", df["has_category"].sum())
    print("Kategori bulunamayan yorum:", (~df["has_category"]).sum())

    print("\nKategori dağılımı:")
    exploded = df.explode("categories")
    print(exploded["categories"].value_counts())

    print("\nKaydedildi:", OUTPUT_PATH)


if __name__ == "__main__":
    analyze()