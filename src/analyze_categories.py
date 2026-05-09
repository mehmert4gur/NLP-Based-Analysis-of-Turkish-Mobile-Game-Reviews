import pandas as pd
import re
from pathlib import Path
from rapidfuzz import fuzz

from category_rules import CATEGORY_RULES

INPUT_PATH = Path("data/processed/temiz_yorumlar.xlsx")
OUTPUT_PATH = Path("data/processed/kategori_analizi.xlsx")

UNCATEGORIZED_PATH = Path("data/processed/kategorisiz_yorumlar.xlsx")
MULTI_CATEGORY_PATH = Path("data/processed/coklu_kategorili_yorumlar.xlsx")
CATEGORY_SAMPLES_PATH = Path("data/processed/kategori_ornekleri.xlsx")
MATCH_DETAILS_PATH = Path("data/processed/kategori_eslesme_detaylari.xlsx")


def tokenize(text):
    if not isinstance(text, str):
        return []
    return text.split()


def keyword_to_pattern(keyword):
    escaped = re.escape(keyword.strip())
    escaped = escaped.replace(r"\ ", r"\s+")
    return rf"(?<!\w){escaped}(?!\w)"


def exact_match(text, keywords):
    for keyword in keywords:
        if not keyword or not isinstance(keyword, str):
            continue

        pattern = keyword_to_pattern(keyword)

        if re.search(pattern, text, flags=re.IGNORECASE):
            return True, keyword

    return False, None


def regex_match(text, patterns):
    for pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True, pattern

    return False, None


def fuzzy_match(text, fuzzy_terms, threshold=88):
    words = tokenize(text)

    for term in fuzzy_terms:
        if not term or len(term) <= 3:
            continue

        for word in words:
            if len(word) <= 3:
                continue

            score = fuzz.ratio(word, term)

            if score >= threshold:
                return True, f"{word} ~ {term} ({score})"

    return False, None


def term_positions(tokens, term):
    """
    Tek kelime veya phrase için token pozisyonlarını döndürür.

    Örnek:
    tokens = ["çok", "zor", "oyun"]
    term = "çok" -> [0]
    term = "zor oyun" -> [1]
    """
    term_tokens = term.split()
    positions = []

    if not term_tokens:
        return positions

    window_size = len(term_tokens)

    for i in range(len(tokens) - window_size + 1):
        if tokens[i:i + window_size] == term_tokens:
            positions.append(i)

    return positions


def near_match(text, near_rules):
    """
    CATEGORY_RULES içindeki near kurallarını işler.

    Desteklenen format:

    "near": [
        {
            "terms": ["çok", "zor"],
            "max_distance": 3
        },
        {
            "terms": ["bölüm", "geçilmiyor"],
            "max_distance": 6
        }
    ]

    Mantık:
    - terms içindeki bütün ifadeler metinde bulunmalı.
    - Bu ifadelerin başlangıç pozisyonları arasındaki maksimum mesafe
      max_distance değerinden küçük/eşit olmalı.
    """
    tokens = tokenize(text)

    if not tokens:
        return False, None

    for rule in near_rules:
        terms = rule.get("terms", [])
        max_distance = rule.get("max_distance", 4)

        if len(terms) < 2:
            continue

        all_positions = []

        for term in terms:
            positions = term_positions(tokens, term)

            if not positions:
                all_positions = []
                break

            all_positions.append(positions)

        if not all_positions:
            continue

        # Şu an 2 veya daha fazla term destekleniyor.
        # Her term için pozisyon kombinasyonlarını kontrol eder.
        def check_combinations(position_lists, current=None):
            if current is None:
                current = []

            if not position_lists:
                return max(current) - min(current) <= max_distance

            for pos in position_lists[0]:
                if check_combinations(position_lists[1:], current + [pos]):
                    return True

            return False

        if check_combinations(all_positions):
            evidence = f"near:{terms}, max_distance:{max_distance}"
            return True, evidence

    return False, None


def find_categories_with_details(text):
    if not isinstance(text, str) or not text.strip():
        return [], []

    found_categories = []
    match_details = []

    for category, rules in CATEGORY_RULES.items():
        keywords = rules.get("keywords", [])
        regex_patterns = rules.get("regex", [])
        near_rules = rules.get("near", [])
        fuzzy_terms = rules.get("fuzzy", [])

        matched, evidence = exact_match(text, keywords)
        if matched:
            found_categories.append(category)
            match_details.append({
                "category": category,
                "match_type": "keyword",
                "evidence": evidence
            })
            continue

        matched, evidence = near_match(text, near_rules)
        if matched:
            found_categories.append(category)
            match_details.append({
                "category": category,
                "match_type": "near",
                "evidence": evidence
            })
            continue

        matched, evidence = regex_match(text, regex_patterns)
        if matched:
            found_categories.append(category)
            match_details.append({
                "category": category,
                "match_type": "regex",
                "evidence": evidence
            })
            continue

        matched, evidence = fuzzy_match(text, fuzzy_terms)
        if matched:
            found_categories.append(category)
            match_details.append({
                "category": category,
                "match_type": "fuzzy",
                "evidence": evidence
            })
            continue

    return found_categories, match_details


def analyze():
    df = pd.read_excel(INPUT_PATH)

    print("Toplam yorum:", len(df))

    if "is_analyzable" not in df.columns:
        raise ValueError(
            "temiz_yorumlar.xlsx içinde 'is_analyzable' sütunu yok. "
            "Önce python src/preprocess_reviews.py çalıştır."
        )

    df = df[df["is_analyzable"] == True].copy()

    print("Analize alınan yorum:", len(df))

    results = df["clean_text"].apply(find_categories_with_details)

    df["categories"] = results.apply(lambda x: x[0])
    df["match_details"] = results.apply(lambda x: x[1])

    df["category_count"] = df["categories"].apply(len)
    df["has_category"] = df["category_count"] > 0

    df.to_excel(OUTPUT_PATH, index=False)

    uncategorized_df = df[df["has_category"] == False].copy()
    uncategorized_df.to_excel(UNCATEGORIZED_PATH, index=False)

    multi_category_df = df[df["category_count"] >= 4].copy()
    multi_category_df.to_excel(MULTI_CATEGORY_PATH, index=False)

    sample_rows = []

    for category in sorted(CATEGORY_RULES.keys()):
        category_df = df[df["categories"].apply(lambda cats: category in cats)].copy()

        if category_df.empty:
            continue

        columns = ["content", "clean_text", "categories", "category_count", "match_details"]

        if "score" in category_df.columns:
            columns.append("score")

        if "app_name" in category_df.columns:
            columns.append("app_name")

        if "review_created_at" in category_df.columns:
            columns.append("review_created_at")

        sample = category_df[columns].head(30).copy()
        sample["sampled_category"] = category

        sample_rows.append(sample)

    if sample_rows:
        category_samples_df = pd.concat(sample_rows, ignore_index=True)
        category_samples_df.to_excel(CATEGORY_SAMPLES_PATH, index=False)

    detail_rows = []

    for _, row in df.iterrows():
        for detail in row["match_details"]:
            detail_row = {
                "content": row.get("content", ""),
                "clean_text": row.get("clean_text", ""),
                "all_categories": row["categories"],
                "category_count": row["category_count"],
                "matched_category": detail["category"],
                "match_type": detail["match_type"],
                "evidence": detail["evidence"],
            }

            if "score" in row.index:
                detail_row["score"] = row.get("score", "")

            if "app_name" in row.index:
                detail_row["app_name"] = row.get("app_name", "")

            if "review_created_at" in row.index:
                detail_row["review_created_at"] = row.get("review_created_at", "")

            detail_rows.append(detail_row)

    match_details_df = pd.DataFrame(detail_rows)
    match_details_df.to_excel(MATCH_DETAILS_PATH, index=False)

    print("Kategori bulunan yorum:", df["has_category"].sum())
    print("Kategori bulunamayan yorum:", (~df["has_category"]).sum())
    print("Çoklu kategori alan yorum:", (df["category_count"] >= 4).sum())

    print("\nKategori dağılımı:")
    exploded = df.explode("categories")
    print(exploded["categories"].value_counts())

    print("\nKaydedilen dosyalar:")
    print("Ana analiz:", OUTPUT_PATH)
    print("Kategorisiz yorumlar:", UNCATEGORIZED_PATH)
    print("Çoklu kategorili yorumlar:", MULTI_CATEGORY_PATH)
    print("Kategori örnekleri:", CATEGORY_SAMPLES_PATH)
    print("Kategori eşleşme detayları:", MATCH_DETAILS_PATH)


if __name__ == "__main__":
    analyze()