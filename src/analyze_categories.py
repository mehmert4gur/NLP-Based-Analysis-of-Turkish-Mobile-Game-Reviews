import pandas as pd
import re
from pathlib import Path
from rapidfuzz import fuzz

from category_rules import CATEGORY_RULES
from sentiment_rules import analyze_sentiment
from aspect_sentiment import infer_local_aspect_sentiments

INPUT_PATH = Path("data/processed/temiz_yorumlar.xlsx")
OUTPUT_PATH = Path("data/processed/kategori_analizi.xlsx")

UNCATEGORIZED_PATH = Path("data/processed/kategorisiz_yorumlar.xlsx")
MULTI_CATEGORY_PATH = Path("data/processed/coklu_kategorili_yorumlar.xlsx")
CATEGORY_SAMPLES_PATH = Path("data/processed/kategori_ornekleri.xlsx")
MATCH_DETAILS_PATH = Path("data/processed/kategori_eslesme_detaylari.xlsx")
SENTIMENT_DETAILS_PATH = Path("data/processed/sentiment_analizi_detaylari.xlsx")
CONTRADICTION_PATH = Path("data/processed/rating_text_contradictions.xlsx")
LOCAL_ASPECT_SENTIMENT_PATH = Path("data/processed/local_aspect_sentiment_details.xlsx")


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


def token_matches(token, term):
    if token == term:
        return True

    if len(term) >= 5 and token.startswith(term):
        return True

    if len(token) >= 5 and term.startswith(token):
        return True

    return False


def term_positions(tokens, term):
    term_tokens = term.split()
    positions = []

    if not term_tokens:
        return positions

    window_size = len(term_tokens)

    for i in range(len(tokens) - window_size + 1):
        window = tokens[i:i + window_size]

        if all(
            token_matches(token, term_token)
            for token, term_token in zip(window, term_tokens)
        ):
            positions.append(i)

    return positions


def near_match(text, near_rules):
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


def get_review_score(row):
    candidate_columns = [
        "score",
        "rating",
        "stars",
        "star",
        "review_score"
    ]

    for column in candidate_columns:
        if column in row.index:
            value = row.get(column, None)

            if pd.notna(value):
                return value

    return None


def add_sentiment_columns(df):
    sentiment_results = []
    local_aspect_results = []

    for _, row in df.iterrows():
        text = row.get("clean_text", "")
        categories = row.get("categories", [])
        match_details = row.get("match_details", [])
        score = get_review_score(row)

        sentiment_result = analyze_sentiment(
            text=text,
            categories=categories,
            score=score
        )

        local_aspect_sentiments, local_aspect_details = infer_local_aspect_sentiments(
            text=text,
            categories=categories,
            match_details=match_details,
            general_sentiment=sentiment_result["general_sentiment"]
        )

        sentiment_results.append(sentiment_result)

        local_aspect_results.append({
            "local_aspect_sentiments": local_aspect_sentiments,
            "local_aspect_sentiment_details": local_aspect_details
        })

    df["general_sentiment"] = [
        result["general_sentiment"] for result in sentiment_results
    ]

    df["sentiment_score"] = [
        result["sentiment_score"] for result in sentiment_results
    ]

    df["positive_score"] = [
        result["positive_score"] for result in sentiment_results
    ]

    df["negative_score"] = [
        result["negative_score"] for result in sentiment_results
    ]

    df["sentiment_evidence"] = [
        result["sentiment_evidence"] for result in sentiment_results
    ]

    df["aspect_sentiments"] = [
        result["aspect_sentiments"] for result in sentiment_results
    ]

    df["aspect_sentiment_details"] = [
        result["aspect_sentiment_details"] for result in sentiment_results
    ]

    df["local_aspect_sentiments"] = [
        result["local_aspect_sentiments"] for result in local_aspect_results
    ]

    df["local_aspect_sentiment_details"] = [
        result["local_aspect_sentiment_details"] for result in local_aspect_results
    ]

    df["rating_text_contradiction"] = [
        result["rating_text_contradiction"] for result in sentiment_results
    ]

    df["contradiction_type"] = [
        result["contradiction_type"] for result in sentiment_results
    ]

    df["contradiction_reason"] = [
        result["contradiction_reason"] for result in sentiment_results
    ]

    return df


def write_category_samples(df):
    sample_rows = []

    for category in sorted(CATEGORY_RULES.keys()):
        category_df = df[df["categories"].apply(lambda cats: category in cats)].copy()

        if category_df.empty:
            continue

        columns = [
            "content",
            "clean_text",
            "categories",
            "category_count",
            "match_details",
            "general_sentiment",
            "aspect_sentiments",
            "local_aspect_sentiments",
            "sentiment_score",
            "sentiment_evidence"
        ]

        for optional_column in ["score", "rating", "app_name", "review_created_at"]:
            if optional_column in category_df.columns:
                columns.append(optional_column)

        sample = category_df[columns].head(30).copy()
        sample["sampled_category"] = category

        sample_rows.append(sample)

    if sample_rows:
        category_samples_df = pd.concat(sample_rows, ignore_index=True)
        category_samples_df.to_excel(CATEGORY_SAMPLES_PATH, index=False)


def write_match_details(df):
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
                "general_sentiment": row.get("general_sentiment", ""),
                "aspect_sentiments": row.get("aspect_sentiments", {}),
                "local_aspect_sentiments": row.get("local_aspect_sentiments", {}),
                "sentiment_score": row.get("sentiment_score", ""),
                "sentiment_evidence": row.get("sentiment_evidence", "")
            }

            for optional_column in ["score", "rating", "app_name", "review_created_at"]:
                if optional_column in row.index:
                    detail_row[optional_column] = row.get(optional_column, "")

            detail_rows.append(detail_row)

    match_details_df = pd.DataFrame(detail_rows)
    match_details_df.to_excel(MATCH_DETAILS_PATH, index=False)


def write_sentiment_details(df):
    columns = [
        "content",
        "clean_text",
        "categories",
        "category_count",
        "general_sentiment",
        "sentiment_score",
        "positive_score",
        "negative_score",
        "sentiment_evidence",
        "aspect_sentiments",
        "aspect_sentiment_details",
        "local_aspect_sentiments",
        "local_aspect_sentiment_details",
        "rating_text_contradiction",
        "contradiction_type",
        "contradiction_reason"
    ]

    for optional_column in ["score", "rating", "app_name", "review_created_at"]:
        if optional_column in df.columns:
            columns.append(optional_column)

    sentiment_df = df[columns].copy()
    sentiment_df.to_excel(SENTIMENT_DETAILS_PATH, index=False)


def write_local_aspect_sentiment_details(df):
    rows = []

    for _, row in df.iterrows():
        details = row.get("local_aspect_sentiment_details", {})

        if not isinstance(details, dict):
            continue

        for category, detail in details.items():
            output_row = {
                "content": row.get("content", ""),
                "clean_text": row.get("clean_text", ""),
                "category": category,
                "local_aspect_sentiment": (
                    row.get("local_aspect_sentiments", {}).get(category, "")
                ),
                "confidence": detail.get("confidence", ""),
                "general_sentiment": row.get("general_sentiment", ""),
                "category_evidence": detail.get("evidence", ""),
                "method": detail.get("method", ""),
                "local_text": detail.get("local_text", ""),
                "local_positive_score": detail.get("local_positive_score", ""),
                "local_negative_score": detail.get("local_negative_score", ""),
                "local_sentiment_score": detail.get("local_sentiment_score", ""),
                "local_evidence": detail.get("local_evidence", "")
            }

            for optional_column in ["score", "rating", "app_name", "review_created_at"]:
                if optional_column in row.index:
                    output_row[optional_column] = row.get(optional_column, "")

            rows.append(output_row)

    local_df = pd.DataFrame(rows)
    local_df.to_excel(LOCAL_ASPECT_SENTIMENT_PATH, index=False)


def write_contradictions(df):
    contradiction_df = df[df["rating_text_contradiction"] == True].copy()

    if contradiction_df.empty:
        pd.DataFrame().to_excel(CONTRADICTION_PATH, index=False)
        return

    columns = [
        "content",
        "clean_text",
        "categories",
        "general_sentiment",
        "sentiment_score",
        "positive_score",
        "negative_score",
        "sentiment_evidence",
        "aspect_sentiments",
        "local_aspect_sentiments",
        "contradiction_type",
        "contradiction_reason"
    ]

    for optional_column in ["score", "rating", "app_name", "review_created_at"]:
        if optional_column in contradiction_df.columns:
            columns.append(optional_column)

    contradiction_df[columns].to_excel(CONTRADICTION_PATH, index=False)


def analyze():
    df = pd.read_excel(INPUT_PATH)

    print("Toplam yorum:", len(df))
    print("Kolonlar:", list(df.columns))

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

    df = add_sentiment_columns(df)

    df.to_excel(OUTPUT_PATH, index=False)

    uncategorized_df = df[df["has_category"] == False].copy()
    uncategorized_df.to_excel(UNCATEGORIZED_PATH, index=False)

    multi_category_df = df[df["category_count"] >= 4].copy()
    multi_category_df.to_excel(MULTI_CATEGORY_PATH, index=False)

    write_category_samples(df)
    write_match_details(df)
    write_sentiment_details(df)
    write_local_aspect_sentiment_details(df)
    write_contradictions(df)

    print("Kategori bulunan yorum:", df["has_category"].sum())
    print("Kategori bulunamayan yorum:", (~df["has_category"]).sum())
    print("Çoklu kategori alan yorum:", (df["category_count"] >= 4).sum())

    print("\nGenel sentiment dağılımı:")
    print(df["general_sentiment"].value_counts())

    print("\nRating-text contradiction sayısı:")
    print(df["rating_text_contradiction"].sum())

    print("\nContradiction reason dağılımı:")
    print(df["contradiction_reason"].value_counts())

    print("\nKategori dağılımı:")
    exploded = df.explode("categories")
    print(exploded["categories"].value_counts())

    print("\nKaydedilen dosyalar:")
    print("Ana analiz:", OUTPUT_PATH)
    print("Kategorisiz yorumlar:", UNCATEGORIZED_PATH)
    print("Çoklu kategorili yorumlar:", MULTI_CATEGORY_PATH)
    print("Kategori örnekleri:", CATEGORY_SAMPLES_PATH)
    print("Kategori eşleşme detayları:", MATCH_DETAILS_PATH)
    print("Sentiment detayları:", SENTIMENT_DETAILS_PATH)
    print("Local aspect sentiment:", LOCAL_ASPECT_SENTIMENT_PATH)
    print("Rating-text contradiction:", CONTRADICTION_PATH)


if __name__ == "__main__":
    analyze()