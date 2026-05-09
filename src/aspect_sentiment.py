# src/aspect_sentiment.py

import ast

from sentiment_rules import (
    score_sentiment_terms,
    classify_category_sentiment,
)


LOCAL_CONTEXT_WINDOW = 7


def tokenize(text):
    if not isinstance(text, str):
        return []
    return text.split()


def safe_parse_evidence(evidence):
    if not isinstance(evidence, str):
        return []

    if not evidence.startswith("near:"):
        return [evidence]

    try:
        terms_part = evidence.split("max_distance")[0]
        terms_part = terms_part.replace("near:", "").strip()
        terms_part = terms_part.rstrip(",").strip()
        parsed = ast.literal_eval(terms_part)

        if isinstance(parsed, list):
            return parsed

    except Exception:
        return []

    return []


def token_matches(token, term):
    if token == term:
        return True

    if len(term) >= 5 and token.startswith(term):
        return True

    if len(token) >= 5 and term.startswith(token):
        return True

    return False


def find_term_positions(tokens, term):
    term_tokens = tokenize(term)
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


def find_evidence_positions(text, evidence):
    tokens = tokenize(text)
    terms = safe_parse_evidence(evidence)

    positions = []

    for term in terms:
        positions.extend(find_term_positions(tokens, term))

    return sorted(set(positions))


def extract_local_context(text, evidence, window=LOCAL_CONTEXT_WINDOW):
    tokens = tokenize(text)

    if not tokens:
        return ""

    positions = find_evidence_positions(text, evidence)

    if not positions:
        return text

    start = max(0, min(positions) - window)
    end = min(len(tokens), max(positions) + window + 1)

    return " ".join(tokens[start:end])


def get_category_evidence(match_details, category):
    for detail in match_details:
        if detail.get("category") == category:
            return detail.get("evidence", "")

    return ""


def calculate_local_confidence(
    method,
    local_positive_score,
    local_negative_score,
    local_text,
    evidence
):
    score_total = local_positive_score + local_negative_score

    if method == "fallback_category_sentiment":
        base = 0.45
    else:
        base = 0.60

    if score_total >= 4:
        base += 0.20
    elif score_total >= 2:
        base += 0.12
    elif score_total >= 1:
        base += 0.06

    if score_total > 0:
        dominance = abs(local_positive_score - local_negative_score) / score_total
        base += dominance * 0.18

    if evidence:
        base += 0.07

    if local_text and len(local_text.split()) <= 18:
        base += 0.05

    confidence = min(base, 0.98)
    confidence = max(confidence, 0.05)

    return round(confidence, 3)


def classify_local_aspect_sentiment(category, full_text, local_text, general_sentiment):
    local_positive, local_negative, local_evidence = score_sentiment_terms(local_text)

    if local_positive > 0 or local_negative > 0:
        final_score = local_positive - local_negative

        if local_positive > 0 and local_negative > 0:
            smaller = min(local_positive, local_negative)
            bigger = max(local_positive, local_negative)
            ratio = smaller / bigger if bigger > 0 else 0

            if ratio >= 0.45:
                label = "mixed"
            elif final_score > 0:
                label = "positive"
            else:
                label = "negative"

        elif final_score > 0:
            label = "positive"

        elif final_score < 0:
            label = "negative"

        else:
            label = "neutral"

        confidence = calculate_local_confidence(
            method="local_context_sentiment",
            local_positive_score=local_positive,
            local_negative_score=local_negative,
            local_text=local_text,
            evidence=local_evidence
        )

        return label, {
            "method": "local_context_sentiment",
            "confidence": confidence,
            "local_positive_score": local_positive,
            "local_negative_score": local_negative,
            "local_sentiment_score": final_score,
            "local_evidence": local_evidence[:12],
            "local_text": local_text
        }

    fallback_label, fallback_details = classify_category_sentiment(
        category=category,
        text=full_text,
        general_sentiment=general_sentiment
    )

    confidence = calculate_local_confidence(
        method="fallback_category_sentiment",
        local_positive_score=local_positive,
        local_negative_score=local_negative,
        local_text=local_text,
        evidence=[]
    )

    return fallback_label, {
        "method": "fallback_category_sentiment",
        "confidence": confidence,
        "local_positive_score": local_positive,
        "local_negative_score": local_negative,
        "local_sentiment_score": 0,
        "local_evidence": [],
        "local_text": local_text,
        "fallback_details": fallback_details
    }


def infer_local_aspect_sentiments(text, categories, match_details, general_sentiment):
    local_aspect_sentiments = {}
    local_aspect_details = {}

    for category in categories:
        evidence = get_category_evidence(match_details, category)
        local_text = extract_local_context(text, evidence)

        sentiment, details = classify_local_aspect_sentiment(
            category=category,
            full_text=text,
            local_text=local_text,
            general_sentiment=general_sentiment
        )

        local_aspect_sentiments[category] = sentiment
        local_aspect_details[category] = {
            "category": category,
            "evidence": evidence,
            **details
        }

    return local_aspect_sentiments, local_aspect_details