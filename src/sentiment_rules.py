# src/sentiment_rules.py

POSITIVE_TERMS = {
    "güzel", "iyi", "harika", "mükemmel", "süper", "efsane", "şahane",
    "keyifli", "eğlenceli", "zevkli", "başarılı", "kaliteli", "beğendim",
    "bayıldım", "sevdim", "seviyorum", "öneririm", "rahatlatıcı",
    "sarıyor", "favori", "favorim", "hoş", "muhteşem", "müq", "mük",
    "excellent", "perfect", "bravo", "teşekkür", "sağlık", "akıcı",
    "sorunsuz", "bedava", "ücretsiz"
}

NEGATIVE_TERMS = {
    "kötü", "berbat", "rezalet", "saçma", "saçmalık", "çöp", "gereksiz",
    "sıkıcı", "bıktım", "bıktırdı", "bunaldım", "sinir", "stres", "nefret",
    "lanet", "sildim", "sileceğim", "silicem", "kaldırıyorum", "indirmeyin",
    "oynamayın", "yüklemeyin", "donuyor", "kasıyor", "açılmıyor",
    "kapanıyor", "çöküyor", "hata", "bug", "bozuk", "bozuldu", "zor",
    "zorlaştı", "zorlaştırıyor", "zorlaştırılmış", "pahalı", "tuzağı",
    "hile", "hileli", "adaletsiz", "haksızlık", "vermiyor", "vermedi",
    "gelmiyor", "azaldı", "azalttı", "azaltıyor", "düşürdü", "düşürüyor",
    "yetmiyor", "kandırmaca", "aldatıcı", "yalan", "alakasız", "uygunsuz",
    "işkence", "eziyet", "mahvoldu", "rezilleşti", "soğudum", "soğuttunuz",
    "oynanmıyor", "oynatmıyor", "oynatmıyorlar", "geçilmiyor", "geçemiyorum",
    "ilerlenmiyor", "kilitli", "kısıtlı", "kısıtlıyor", "boşa", "kaybı",
    "kabus", "adilik", "kumar", "kumara", "hak", "etmiyorsunuz"
}

NEGATION_TERMS = {
    "değil", "degil", "yok", "olmuyor", "olmadı", "olmaz",
    "istemiyor", "istemem", "sevmiyorum", "beğenmedim",
    "etmiyorum", "etmem", "deyil"
}

INTENSIFIERS = {
    "çok", "aşırı", "fazla", "acayip", "gerçekten", "resmen", "tamamen",
    "kesinlikle", "iyice", "çokkk", "çook", "cok", "cokk"
}

POSITIVE_PHRASES = {
    "çok güzel",
    "çok iyi",
    "harika oyun",
    "güzel oyun",
    "mükemmel oyun",
    "tavsiye ederim",
    "tavsiye ediyorum",
    "herkese öneririm",
    "herkese tavsiye ederim",
    "elinize sağlık",
    "ellerinize sağlık",
    "emeğinize sağlık",
    "sorunsuz çalışıyor",
    "akıcı çalışıyor",
    "reklam yok",
    "reklamsız",
    "para istemiyor",
    "ücretsiz oyun",
    "bedava oyun"
}

NEGATIVE_PHRASES = {
    "tavsiye etmiyorum",
    "tavsiye etmem",
    "önermiyorum",
    "hiç iyi değil",
    "iyi değil",
    "güzel değil",
    "oynamayın",
    "indirmeyin",
    "yüklemeyin",
    "zaman kaybı",
    "vakit kaybı",
    "para tuzağı",
    "çok reklam",
    "aşırı reklam",
    "fazla reklam",
    "satın almaya zorluyor",
    "para harcamaya zorluyor",
    "para yatırmaya zorluyor",
    "oyun açılmıyor",
    "oyuna girilmiyor",
    "oyundan atıyor",
    "bölüm geçilmiyor",
    "çok zor",
    "aşırı zor",
    "ödüller azaldı",
    "kart vermiyor",
    "kart vermedi",
    "reklamdaki gibi değil",
    "reklamla alakası yok",
    "görselle oyunun alakası yok",
    "kumara döndü",
    "kumar gibi",
    "hileli oyun",
    "oyun hileli",
    "oynatmıyorlar",
    "hak etmiyorsunuz"
}

NEGATIVE_DEFAULT_CATEGORIES = {
    "reklam",
    "yaniltici_reklam_tanitim",
    "guncelleme_sorunu",
    "cihaz_goruntu_sorunu",
    "yukleme_acilis_sorunu",
    "performans_donma_kasma",
    "crash_hata_bug",
    "zorluk_level_design",
    "can_hamle_hak_sure",
    "odeme_satin_alma_ekonomi",
    "odul_bonus_ipucu",
    "kart_koleksiyon",
    "hile_algoritma_adalet",
    "destek_iletisim",
    "hesap_kayit_ilerleme",
    "gizlilik_guvenlik_izin",
    "dil_lokalizasyon",
    "uygunsuz_icerik_yas",
    "genel_negatif_deneyim",
}

POSITIVE_DEFAULT_CATEGORIES = {
    "olumlu_deneyim",
    "egitici_bilissel_fayda",
}

NEUTRAL_DEFAULT_CATEGORIES = {
    "internet_cevrimdisi",
    "gelistirme_onerisi",
    "sohbet_takim_arkadas_topluluk",
    "yeni_bolum_icerik_eksikligi",
    "rating_manipulation",
    "spam_anlamsiz",
}


CATEGORY_POSITIVE_PATTERNS = {
    "reklam": [
        "reklam yok",
        "reklam çıkmıyor",
        "reklam gelmiyor",
        "reklamsız",
        "reklam sorun değil",
        "reklam sıkıntı değil",
        "reklam rahatsız etmiyor",
        "reklam az"
    ],
    "odeme_satin_alma_ekonomi": [
        "para istemiyor",
        "ücretsiz",
        "bedava",
        "para harcamadan",
        "satın almadan",
        "para yatırmadan",
        "para vermeden"
    ],
    "internet_cevrimdisi": [
        "internetsiz oynanıyor",
        "internet olmadan oynanıyor",
        "çevrimdışı oynanıyor",
        "offline oynanıyor"
    ],
    "performans_donma_kasma": [
        "kasmıyor",
        "donmuyor",
        "akıcı",
        "sorunsuz çalışıyor"
    ],
    "yukleme_acilis_sorunu": [
        "açılıyor",
        "sorunsuz açılıyor",
        "hemen açılıyor"
    ],
}

CATEGORY_NEGATIVE_PATTERNS = {
    "reklam": [
        "çok reklam",
        "fazla reklam",
        "aşırı reklam",
        "sürekli reklam",
        "reklamdan oynanmıyor",
        "reklam yüzünden",
        "reklam izletiyor",
        "reklamından kurtulsam",
        "reklamdan kurtulsam"
    ],
    "yaniltici_reklam_tanitim": [
        "reklamdaki gibi değil",
        "reklamla alakası yok",
        "reklamdaki oyun yok",
        "görselle oyunun alakası yok",
        "görsel ile oyunun alakası yok",
        "reklamlarda gösterdikleri oyunları oynatmıyorlar"
    ],
    "odeme_satin_alma_ekonomi": [
        "para tuzağı",
        "para harcatıyor",
        "para harcamaya zorluyor",
        "parayla geçiliyor",
        "parasız ilerlenmiyor",
        "pahalı",
        "satın almaya zorluyor",
        "altın almaya zorluyor",
        "kumara döndü",
        "kumar gibi"
    ],
    "zorluk_level_design": [
        "çok zor",
        "aşırı zor",
        "geçemiyorum",
        "geçilmiyor",
        "zorlaştırıyor",
        "zorlaştırılmış",
        "zorlaştı",
        "sıkıcı",
        "stres",
        "günlerce sürüyor",
        "günlerce geçemiyorum"
    ],
    "odul_bonus_ipucu": [
        "ödül az",
        "ödüller azaldı",
        "hediye gelmiyor",
        "kart vermiyor",
        "kart vermedi",
        "altın az",
        "puan az"
    ],
    "kart_koleksiyon": [
        "kart vermiyor",
        "kart vermedi",
        "kart gelmiyor",
        "kart çıkmıyor",
        "aynı kart",
        "koleksiyon tamamlanmıyor"
    ],
    "hile_algoritma_adalet": [
        "hile",
        "hileli",
        "algoritma",
        "adaletsiz",
        "sistem engelliyor",
        "bilerek",
        "müdahale",
        "kaybettiriyor"
    ],
}


def tokenize(text):
    if not isinstance(text, str):
        return []
    return text.split()


def token_matches(token, term):
    """
    Sentiment tarafında ters prefix yok.

    Doğru:
    güzel -> güzeldi
    zor -> zorlaştı

    Yanlış olmaması gereken:
    reklam -> reklamsız
    sorun -> sorunsuz
    """
    if token == term:
        return True

    if len(term) >= 5 and len(token) > len(term) and token.startswith(term):
        return True

    return False


def contains_phrase(text, phrase):
    text_tokens = tokenize(text)
    phrase_tokens = tokenize(phrase)

    if not phrase_tokens:
        return False

    window_size = len(phrase_tokens)

    for i in range(len(text_tokens) - window_size + 1):
        window = text_tokens[i:i + window_size]

        if all(
            token_matches(token, phrase_token)
            for token, phrase_token in zip(window, phrase_tokens)
        ):
            return True

    return False


def has_negation_near(tokens, index, window=3):
    start = max(0, index - window)
    end = min(len(tokens), index + window + 1)

    context = tokens[start:end]
    joined_context = " ".join(context)

    for negation in NEGATION_TERMS:
        if negation in context or negation in joined_context:
            return True

    return False


def phrase_sentiment_score(text):
    positive_score = 0
    negative_score = 0
    evidence = []

    for phrase in POSITIVE_PHRASES:
        if contains_phrase(text, phrase):
            positive_score += 2
            evidence.append(f"positive_phrase:{phrase}")

    for phrase in NEGATIVE_PHRASES:
        if contains_phrase(text, phrase):
            negative_score += 2
            evidence.append(f"negative_phrase:{phrase}")

    return positive_score, negative_score, evidence


def score_sentiment_terms(text):
    tokens = tokenize(text)

    positive_score, negative_score, evidence = phrase_sentiment_score(text)

    for i, token in enumerate(tokens):
        multiplier = 1

        if i > 0 and tokens[i - 1] in INTENSIFIERS:
            multiplier = 2

        matched_positive = any(token_matches(token, term) for term in POSITIVE_TERMS)
        matched_negative = any(token_matches(token, term) for term in NEGATIVE_TERMS)

        negated = has_negation_near(tokens, i)

        if matched_positive:
            if negated:
                negative_score += multiplier
                evidence.append(f"negated_positive:{token}")
            else:
                positive_score += multiplier
                evidence.append(f"positive:{token}")

        if matched_negative:
            if negated:
                evidence.append(f"neutralized_negative:{token}")
            else:
                negative_score += multiplier
                evidence.append(f"negative:{token}")

    return positive_score, negative_score, evidence


def classify_general_sentiment(text):
    positive_score, negative_score, evidence = score_sentiment_terms(text)

    if positive_score == 0 and negative_score == 0:
        return {
            "general_sentiment": "neutral",
            "sentiment_score": 0,
            "positive_score": 0,
            "negative_score": 0,
            "sentiment_evidence": []
        }

    final_score = positive_score - negative_score

    if positive_score > 0 and negative_score > 0:
        smaller = min(positive_score, negative_score)
        bigger = max(positive_score, negative_score)
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

    return {
        "general_sentiment": label,
        "sentiment_score": final_score,
        "positive_score": positive_score,
        "negative_score": negative_score,
        "sentiment_evidence": evidence[:25]
    }


def classify_category_sentiment(category, text, general_sentiment):
    positive_patterns = CATEGORY_POSITIVE_PATTERNS.get(category, [])
    negative_patterns = CATEGORY_NEGATIVE_PATTERNS.get(category, [])

    positive_hits = [
        pattern for pattern in positive_patterns
        if contains_phrase(text, pattern)
    ]

    negative_hits = [
        pattern for pattern in negative_patterns
        if contains_phrase(text, pattern)
    ]

    if positive_hits and negative_hits:
        return "mixed", {
            "positive_evidence": positive_hits,
            "negative_evidence": negative_hits,
            "reason": "category_specific_positive_and_negative"
        }

    if positive_hits:
        return "positive", {
            "positive_evidence": positive_hits,
            "negative_evidence": [],
            "reason": "category_specific_positive"
        }

    if negative_hits:
        return "negative", {
            "positive_evidence": [],
            "negative_evidence": negative_hits,
            "reason": "category_specific_negative"
        }

    if category in POSITIVE_DEFAULT_CATEGORIES:
        return "positive", {
            "positive_evidence": [],
            "negative_evidence": [],
            "reason": "positive_default_category"
        }

    if category in NEGATIVE_DEFAULT_CATEGORIES:
        return "negative", {
            "positive_evidence": [],
            "negative_evidence": [],
            "reason": "negative_default_category"
        }

    if category in NEUTRAL_DEFAULT_CATEGORIES:
        return general_sentiment, {
            "positive_evidence": [],
            "negative_evidence": [],
            "reason": "neutral_category_inherits_general_sentiment"
        }

    return "unknown", {
        "positive_evidence": [],
        "negative_evidence": [],
        "reason": "unknown_category"
    }


def infer_aspect_sentiments(text, categories, general_sentiment):
    aspect_sentiments = {}
    aspect_sentiment_details = {}

    for category in categories:
        sentiment, details = classify_category_sentiment(
            category=category,
            text=text,
            general_sentiment=general_sentiment
        )

        aspect_sentiments[category] = sentiment
        aspect_sentiment_details[category] = details

    return aspect_sentiments, aspect_sentiment_details


def detect_rating_text_contradiction(score, general_sentiment, sentiment_score):
    if score is None:
        return {
            "rating_text_contradiction": False,
            "contradiction_type": "",
            "contradiction_reason": "score_missing"
        }

    try:
        numeric_score = float(score)
    except (TypeError, ValueError):
        return {
            "rating_text_contradiction": False,
            "contradiction_type": "",
            "contradiction_reason": "score_not_numeric"
        }

    if numeric_score == 5 and sentiment_score <= -3:
        return {
            "rating_text_contradiction": True,
            "contradiction_type": "five_star_strong_negative_text",
            "contradiction_reason": "score=5 and sentiment_score<=-3"
        }

    if numeric_score == 4 and sentiment_score <= -4:
        return {
            "rating_text_contradiction": True,
            "contradiction_type": "four_star_strong_negative_text",
            "contradiction_reason": "score=4 and sentiment_score<=-4"
        }

    if numeric_score == 1 and sentiment_score >= 3:
        return {
            "rating_text_contradiction": True,
            "contradiction_type": "one_star_strong_positive_text",
            "contradiction_reason": "score=1 and sentiment_score>=3"
        }

    if numeric_score == 2 and sentiment_score >= 4:
        return {
            "rating_text_contradiction": True,
            "contradiction_type": "two_star_strong_positive_text",
            "contradiction_reason": "score=2 and sentiment_score>=4"
        }

    return {
        "rating_text_contradiction": False,
        "contradiction_type": "",
        "contradiction_reason": "no_contradiction"
    }


def analyze_sentiment(text, categories, score=None):
    general = classify_general_sentiment(text)

    aspect_sentiments, aspect_details = infer_aspect_sentiments(
        text=text,
        categories=categories,
        general_sentiment=general["general_sentiment"]
    )

    contradiction = detect_rating_text_contradiction(
        score=score,
        general_sentiment=general["general_sentiment"],
        sentiment_score=general["sentiment_score"]
    )

    return {
        **general,
        "aspect_sentiments": aspect_sentiments,
        "aspect_sentiment_details": aspect_details,
        **contradiction
    }