from pathlib import Path
import json

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from analyze_categories import find_categories_with_details
from sentiment_rules import analyze_sentiment
from aspect_sentiment import infer_local_aspect_sentiments


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = (
    BASE_DIR
    / "outputs"
    / "models"
    / "berturk_multilabel_absa_full"
    / "best_model"
).resolve()

MAX_LENGTH = 128

BERT_THRESHOLD = 0.35
HIGH_CONFIDENCE_THRESHOLD = 0.60
MEDIUM_CONFIDENCE_THRESHOLD = 0.45
UNCERTAIN_LOWER_THRESHOLD = 0.25
UNCERTAIN_UPPER_THRESHOLD = 0.35

TOP_K = 8


CATEGORY_DISPLAY_NAMES = {
    "rating_manipulation": "Rating manipülasyonu",
    "reklam": "Reklam",
    "yaniltici_reklam_tanitim": "Yanıltıcı reklam / tanıtım",
    "guncelleme_sorunu": "Güncelleme sorunu",
    "yeni_bolum_icerik_eksikligi": "Yeni bölüm / içerik eksikliği",
    "cihaz_goruntu_sorunu": "Cihaz / görüntü sorunu",
    "yukleme_acilis_sorunu": "Yükleme / açılış sorunu",
    "performans_donma_kasma": "Performans / donma / kasma",
    "crash_hata_bug": "Crash / hata / bug",
    "zorluk_level_design": "Zorluk / level tasarımı",
    "can_hamle_hak_sure": "Can / hamle / süre",
    "odeme_satin_alma_ekonomi": "Ödeme / satın alma / ekonomi",
    "odul_bonus_ipucu": "Ödül / bonus / ipucu",
    "kart_koleksiyon": "Kart / koleksiyon",
    "hile_algoritma_adalet": "Hile / algoritma / adalet",
    "destek_iletisim": "Destek / iletişim",
    "sohbet_takim_arkadas_topluluk": "Sohbet / takım / topluluk",
    "hesap_kayit_ilerleme": "Hesap / kayıt / ilerleme",
    "internet_cevrimdisi": "İnternet / çevrimdışı",
    "gizlilik_guvenlik_izin": "Gizlilik / güvenlik / izin",
    "dil_lokalizasyon": "Dil / lokalizasyon",
    "uygunsuz_icerik_yas": "Uygunsuz içerik / yaş",
    "egitici_bilissel_fayda": "Eğitici / bilişsel fayda",
    "olumlu_deneyim": "Olumlu deneyim",
    "genel_negatif_deneyim": "Genel negatif deneyim",
    "gelistirme_onerisi": "Geliştirme önerisi",
    "spam_anlamsiz": "Spam / anlamsız",
}


CATEGORY_TEAMS = {
    "reklam": "Monetization / Product",
    "yaniltici_reklam_tanitim": "Marketing / Product",
    "performans_donma_kasma": "Engineering / Performance",
    "crash_hata_bug": "Engineering / QA",
    "yukleme_acilis_sorunu": "Engineering / Backend / QA",
    "cihaz_goruntu_sorunu": "Engineering / Graphics / QA",
    "odeme_satin_alma_ekonomi": "Monetization / Payments",
    "odul_bonus_ipucu": "Game Economy / Product",
    "kart_koleksiyon": "Game Economy / Product",
    "zorluk_level_design": "Game Design / Product",
    "can_hamle_hak_sure": "Game Design / Economy",
    "hile_algoritma_adalet": "Game Design / Fairness / Analytics",
    "destek_iletisim": "Customer Support",
    "hesap_kayit_ilerleme": "Account / Backend / Support",
    "gizlilik_guvenlik_izin": "Security / Legal",
    "uygunsuz_icerik_yas": "Trust & Safety / Content",
    "dil_lokalizasyon": "Localization",
    "internet_cevrimdisi": "Engineering / Connectivity",
    "guncelleme_sorunu": "Release / QA",
    "yeni_bolum_icerik_eksikligi": "Content / Product",
    "sohbet_takim_arkadas_topluluk": "Community / Social Features",
    "gelistirme_onerisi": "Product",
    "olumlu_deneyim": "Product / Marketing",
    "genel_negatif_deneyim": "Product",
    "egitici_bilissel_fayda": "Product / Marketing",
    "rating_manipulation": "Data Quality",
    "spam_anlamsiz": "Data Quality",
}


HIGH_PRIORITY_CATEGORIES = {
    "odeme_satin_alma_ekonomi",
    "gizlilik_guvenlik_izin",
    "uygunsuz_icerik_yas",
    "crash_hata_bug",
    "yukleme_acilis_sorunu",
    "hesap_kayit_ilerleme",
    "hile_algoritma_adalet",
}


ACTION_SUGGESTIONS = {
    "reklam": "Reklam sıklığı, reklam süresi ve reklam yerleşimleri incelenmeli.",
    "yaniltici_reklam_tanitim": "Reklam kreatifleri ile gerçek oyun deneyimi arasındaki tutarlılık kontrol edilmeli.",
    "performans_donma_kasma": "Cihaz bazlı performans, FPS, bellek kullanımı ve donma raporları incelenmeli.",
    "crash_hata_bug": "Crash logları, hata senaryoları ve kullanıcı akışı QA ekibi tarafından kontrol edilmeli.",
    "yukleme_acilis_sorunu": "Açılış, loading ve bağlantı süreçleri teknik olarak incelenmeli.",
    "cihaz_goruntu_sorunu": "Cihaz uyumluluğu, çözünürlük ve grafik render sorunları kontrol edilmeli.",
    "odeme_satin_alma_ekonomi": "Fiyatlandırma, satın alma akışı, iade şikayetleri ve pay-to-win algısı incelenmeli.",
    "odul_bonus_ipucu": "Ödül dengesi, bonus miktarı ve kullanıcıya verilen kaynaklar gözden geçirilmeli.",
    "kart_koleksiyon": "Kart düşme oranları, koleksiyon tamamlama akışı ve tekrar eden kart sistemi incelenmeli.",
    "zorluk_level_design": "Zorluk eğrisi, level geçme oranları ve hamle dengesi analiz edilmeli.",
    "can_hamle_hak_sure": "Can, hamle ve süre kısıtlarının kullanıcı deneyimine etkisi ölçülmeli.",
    "hile_algoritma_adalet": "Oyuncuda adaletsizlik veya manipülasyon algısı yaratan mekanikler incelenmeli.",
    "destek_iletisim": "Destek yanıt süreleri ve kullanıcı iletişim kanalları iyileştirilmeli.",
    "hesap_kayit_ilerleme": "Hesap kurtarma, ilerleme kaybı ve senkronizasyon süreçleri kontrol edilmeli.",
    "gizlilik_guvenlik_izin": "İzinler, veri kullanımı ve güvenlik algısı açısından ürün incelenmeli.",
    "uygunsuz_icerik_yas": "İçerik, reklam ve yaş uygunluğu açısından güvenlik kontrolü yapılmalı.",
    "dil_lokalizasyon": "Türkçe çeviri, menü metinleri ve lokalizasyon kalitesi gözden geçirilmeli.",
    "internet_cevrimdisi": "Çevrimdışı oynanabilirlik ve bağlantı hataları analiz edilmeli.",
    "guncelleme_sorunu": "Son sürüm sonrası oluşan hata, performans veya deneyim değişiklikleri incelenmeli.",
    "yeni_bolum_icerik_eksikligi": "Yeni bölüm, yeni etkinlik ve içerik beklentisi ürün planına alınmalı.",
    "sohbet_takim_arkadas_topluluk": "Sosyal özellikler, takım sistemi ve sohbet akışı kontrol edilmeli.",
    "gelistirme_onerisi": "Kullanıcının önerisi ürün backlog’una aday olarak değerlendirilmeli.",
    "olumlu_deneyim": "Olumlu deneyim unsurları pazarlama ve ürün iletişiminde kullanılabilir.",
    "genel_negatif_deneyim": "Genel memnuniyetsizlik yaratan ana nedenler detaylı incelenmeli.",
    "egitici_bilissel_fayda": "Eğitici ve bilişsel fayda vurgusu ürün konumlandırmasında kullanılabilir.",
    "rating_manipulation": "Rating ile yorum metni arasındaki manipülasyon ihtimali veri kalitesi açısından işaretlenmeli.",
    "spam_anlamsiz": "Yorum analiz dışı bırakılabilir veya düşük güvenli veri olarak işaretlenebilir.",
}


def load_model():
    if not MODEL_DIR.exists():
        raise FileNotFoundError(f"Model klasörü bulunamadı: {MODEL_DIR}")

    tokenizer = AutoTokenizer.from_pretrained(
        str(MODEL_DIR),
        local_files_only=True,
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        str(MODEL_DIR),
        local_files_only=True,
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model.to(device)
    model.eval()

    return tokenizer, model, device


def get_display_name(category):
    return CATEGORY_DISPLAY_NAMES.get(category, category)


def get_confidence_level(probability):
    if probability >= HIGH_CONFIDENCE_THRESHOLD:
        return "high"
    if probability >= MEDIUM_CONFIDENCE_THRESHOLD:
        return "medium"
    if probability >= BERT_THRESHOLD:
        return "low"
    return "below_threshold"


def predict_berturk_categories(text, tokenizer, model, device):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH,
    )

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.sigmoid(outputs.logits[0]).cpu()

    predictions = {}

    for idx, prob in enumerate(probs):
        label = model.config.id2label[idx]
        predictions[label] = float(prob)

    return predictions


def hybrid_decision(rule_categories, bert_probs):
    final_categories = set(rule_categories)
    decision_details = []

    rule_categories = set(rule_categories)

    for category, probability in bert_probs.items():
        if probability >= HIGH_CONFIDENCE_THRESHOLD:
            final_categories.add(category)
            decision_details.append({
                "category": category,
                "display_name": get_display_name(category),
                "source": "bert_high_confidence",
                "probability": round(probability, 4),
                "confidence_level": get_confidence_level(probability),
            })

        elif probability >= BERT_THRESHOLD and category in rule_categories:
            final_categories.add(category)
            decision_details.append({
                "category": category,
                "display_name": get_display_name(category),
                "source": "rule_and_bert_agree",
                "probability": round(probability, 4),
                "confidence_level": get_confidence_level(probability),
            })

    for category in rule_categories:
        if not any(detail["category"] == category for detail in decision_details):
            probability = bert_probs.get(category, 0)

            decision_details.append({
                "category": category,
                "display_name": get_display_name(category),
                "source": "rule_based",
                "probability": round(probability, 4),
                "confidence_level": get_confidence_level(probability),
            })

    return sorted(final_categories), decision_details


def get_top_bert_predictions(bert_probs, top_k=TOP_K):
    return [
        {
            "category": category,
            "display_name": get_display_name(category),
            "probability": round(probability, 4),
            "confidence_level": get_confidence_level(probability),
        }
        for category, probability in sorted(
            bert_probs.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:top_k]
    ]


def get_uncertain_predictions(bert_probs, final_categories):
    uncertain = []

    for category, probability in bert_probs.items():
        if category in final_categories:
            continue

        if UNCERTAIN_LOWER_THRESHOLD <= probability < UNCERTAIN_UPPER_THRESHOLD:
            uncertain.append({
                "category": category,
                "display_name": get_display_name(category),
                "probability": round(probability, 4),
                "reason": "threshold_altında ama dikkat çekici olasılık",
            })

    return sorted(
        uncertain,
        key=lambda item: item["probability"],
        reverse=True,
    )[:5]


def calculate_agreement_score(rule_categories, bert_probs):
    rule_set = set(rule_categories)

    bert_set = {
        category
        for category, probability in bert_probs.items()
        if probability >= BERT_THRESHOLD
    }

    union = rule_set | bert_set
    intersection = rule_set & bert_set

    if not union:
        return {
            "score": 1.0,
            "common_categories": [],
            "rule_only_categories": [],
            "bert_only_categories": [],
            "interpretation": "Rule-based sistem ve BERTürk ikisi de kategori bulmadı.",
        }

    score = len(intersection) / len(union)

    if score >= 0.75:
        interpretation = "Rule-based sistem ve BERTürk yüksek oranda uyumlu."
    elif score >= 0.40:
        interpretation = "Rule-based sistem ve BERTürk kısmen uyumlu."
    else:
        interpretation = "Rule-based sistem ve BERTürk arasında belirgin fark var."

    return {
        "score": round(score, 4),
        "common_categories": sorted(intersection),
        "rule_only_categories": sorted(rule_set - bert_set),
        "bert_only_categories": sorted(bert_set - rule_set),
        "interpretation": interpretation,
    }


def summarize_confidence(final_categories, bert_probs):
    summary = {
        "high": 0,
        "medium": 0,
        "low": 0,
        "rule_only_or_below_threshold": 0,
    }

    details = []

    for category in final_categories:
        probability = bert_probs.get(category, 0)
        level = get_confidence_level(probability)

        if level == "high":
            summary["high"] += 1
        elif level == "medium":
            summary["medium"] += 1
        elif level == "low":
            summary["low"] += 1
        else:
            summary["rule_only_or_below_threshold"] += 1

        details.append({
            "category": category,
            "display_name": get_display_name(category),
            "probability": round(probability, 4),
            "confidence_level": level,
        })

    return {
        "summary": summary,
        "details": details,
    }


def summarize_aspect_sentiments(aspect_sentiments):
    counts = {
        "positive": 0,
        "negative": 0,
        "neutral": 0,
        "mixed": 0,
        "unknown": 0,
    }

    for sentiment in aspect_sentiments.values():
        counts[sentiment] = counts.get(sentiment, 0) + 1

    return counts


def create_explanations(rule_match_details, decision_details, bert_probs):
    explanations = {}
    evidence_by_category = {}

    for detail in rule_match_details:
        category = detail.get("category")
        if not category:
            continue

        evidence_by_category.setdefault(category, []).append({
            "match_type": detail.get("match_type", ""),
            "evidence": detail.get("evidence", ""),
        })

    for detail in decision_details:
        category = detail["category"]
        probability = bert_probs.get(category, 0)
        source = detail["source"]

        if source == "rule_and_bert_agree":
            explanation_text = "Rule-based sistem kategori buldu ve BERTürk de eşik üstü olasılık verdi."
        elif source == "bert_high_confidence":
            explanation_text = "BERTürk modeli bu kategoriyi yüksek güvenle tahmin etti."
        elif source == "rule_based":
            explanation_text = "Kategori rule-based sistem tarafından yakalandı."
        else:
            explanation_text = "Kategori hybrid karar mekanizması tarafından seçildi."

        explanations[category] = {
            "category": category,
            "display_name": get_display_name(category),
            "source": source,
            "probability": round(probability, 4),
            "confidence_level": get_confidence_level(probability),
            "explanation": explanation_text,
            "rule_evidence": evidence_by_category.get(category, []),
        }

    return explanations


def calculate_severity(category, sentiment, probability):
    if category in HIGH_PRIORITY_CATEGORIES:
        if sentiment == "negative" or probability >= HIGH_CONFIDENCE_THRESHOLD:
            return "high"
        return "medium"

    if sentiment == "negative" and probability >= HIGH_CONFIDENCE_THRESHOLD:
        return "high"

    if sentiment in {"negative", "mixed"}:
        return "medium"

    return "low"


def create_product_insights(final_categories, aspect_sentiments, bert_probs):
    insights = []

    for category in final_categories:
        sentiment = aspect_sentiments.get(category, "unknown")
        probability = bert_probs.get(category, 0)

        insights.append({
            "category": category,
            "display_name": get_display_name(category),
            "sentiment": sentiment,
            "probability": round(probability, 4),
            "severity": calculate_severity(category, sentiment, probability),
            "team": CATEGORY_TEAMS.get(category, "Product"),
            "suggested_action": ACTION_SUGGESTIONS.get(
                category,
                "Kategori ürün ekibi tarafından incelenmeli."
            ),
        })

    severity_order = {
        "high": 3,
        "medium": 2,
        "low": 1,
    }

    insights = sorted(
        insights,
        key=lambda item: (
            severity_order.get(item["severity"], 0),
            item["probability"],
        ),
        reverse=True,
    )

    return {
        "main_issue": insights[0] if insights else None,
        "all_insights": insights,
    }


def create_warnings(
    final_categories,
    sentiment_result,
    uncertain_predictions,
    agreement_result,
):
    warnings = []

    if sentiment_result.get("rating_text_contradiction", False):
        warnings.append({
            "type": "rating_text_contradiction",
            "level": "high",
            "message": "Kullanıcının verdiği yıldız puanı ile yorum metnindeki duygu çelişiyor.",
            "details": {
                "contradiction_type": sentiment_result.get("contradiction_type", ""),
                "contradiction_reason": sentiment_result.get("contradiction_reason", ""),
            },
        })

    risky_categories = sorted(set(final_categories) & HIGH_PRIORITY_CATEGORIES)

    if risky_categories:
        warnings.append({
            "type": "high_priority_category",
            "level": "high",
            "message": "Yorumda öncelikli incelenmesi gereken kategori bulundu.",
            "details": {
                "categories": risky_categories,
                "display_names": [get_display_name(category) for category in risky_categories],
            },
        })

    if uncertain_predictions:
        warnings.append({
            "type": "uncertain_predictions",
            "level": "medium",
            "message": "Modelin eşik altında kalan ama dikkat çekici bazı tahminleri var.",
            "details": uncertain_predictions,
        })

    if agreement_result["score"] < 0.40:
        warnings.append({
            "type": "low_rule_bert_agreement",
            "level": "medium",
            "message": "Rule-based sistem ile BERTürk tahminleri arasında düşük uyum var.",
            "details": agreement_result,
        })

    return warnings


def analyze_review_for_ui(text, rating=None, tokenizer=None, model=None, device=None):
    if not isinstance(text, str) or not text.strip():
        return {
            "success": False,
            "error": "Boş metin analiz edilemez.",
        }

    if tokenizer is None or model is None or device is None:
        tokenizer, model, device = load_model()

    clean_input_text = text.strip()

    rule_categories, rule_match_details = find_categories_with_details(clean_input_text)

    bert_probs = predict_berturk_categories(
        text=clean_input_text,
        tokenizer=tokenizer,
        model=model,
        device=device,
    )

    final_categories, decision_details = hybrid_decision(
        rule_categories=rule_categories,
        bert_probs=bert_probs,
    )

    sentiment_result = analyze_sentiment(
        text=clean_input_text,
        categories=final_categories,
        score=rating,
    )

    local_aspect_sentiments, local_aspect_details = infer_local_aspect_sentiments(
        text=clean_input_text,
        categories=final_categories,
        match_details=rule_match_details,
        general_sentiment=sentiment_result["general_sentiment"],
    )

    top_bert_predictions = get_top_bert_predictions(bert_probs)
    uncertain_predictions = get_uncertain_predictions(bert_probs, final_categories)

    agreement_result = calculate_agreement_score(
        rule_categories=rule_categories,
        bert_probs=bert_probs,
    )

    confidence_result = summarize_confidence(
        final_categories=final_categories,
        bert_probs=bert_probs,
    )

    aspect_sentiment_summary = summarize_aspect_sentiments(
        sentiment_result.get("aspect_sentiments", {})
    )

    local_aspect_sentiment_summary = summarize_aspect_sentiments(
        local_aspect_sentiments
    )

    explanations = create_explanations(
        rule_match_details=rule_match_details,
        decision_details=decision_details,
        bert_probs=bert_probs,
    )

    product_insights = create_product_insights(
        final_categories=final_categories,
        aspect_sentiments=sentiment_result.get("aspect_sentiments", {}),
        bert_probs=bert_probs,
    )

    warnings = create_warnings(
        final_categories=final_categories,
        sentiment_result=sentiment_result,
        uncertain_predictions=uncertain_predictions,
        agreement_result=agreement_result,
    )

    return {
        "success": True,

        "input": {
            "text": clean_input_text,
            "rating": rating,
            "text_length": len(clean_input_text),
            "word_count": len(clean_input_text.split()),
        },

        "categories": {
            "final_categories": [
                {
                    "category": category,
                    "display_name": get_display_name(category),
                    "probability": round(bert_probs.get(category, 0), 4),
                    "confidence_level": get_confidence_level(bert_probs.get(category, 0)),
                }
                for category in final_categories
            ],
            "rule_categories": [
                {
                    "category": category,
                    "display_name": get_display_name(category),
                }
                for category in rule_categories
            ],
            "bert_top_predictions": top_bert_predictions,
            "uncertain_predictions": uncertain_predictions,
            "decision_details": decision_details,
            "rule_match_details": rule_match_details,
        },

        "sentiment": {
            "general_sentiment": sentiment_result["general_sentiment"],
            "sentiment_score": sentiment_result["sentiment_score"],
            "positive_score": sentiment_result["positive_score"],
            "negative_score": sentiment_result["negative_score"],
            "sentiment_evidence": sentiment_result["sentiment_evidence"],
            "aspect_sentiments": sentiment_result.get("aspect_sentiments", {}),
            "aspect_sentiment_details": sentiment_result.get("aspect_sentiment_details", {}),
            "local_aspect_sentiments": local_aspect_sentiments,
            "local_aspect_sentiment_details": local_aspect_details,
            "rating_text_contradiction": sentiment_result.get("rating_text_contradiction", False),
            "contradiction_type": sentiment_result.get("contradiction_type", ""),
            "contradiction_reason": sentiment_result.get("contradiction_reason", ""),
        },

        "statistics": {
            "final_category_count": len(final_categories),
            "rule_category_count": len(rule_categories),
            "bert_threshold_category_count": len([
                category
                for category, probability in bert_probs.items()
                if probability >= BERT_THRESHOLD
            ]),
            "agreement": agreement_result,
            "confidence": confidence_result,
            "aspect_sentiment_summary": aspect_sentiment_summary,
            "local_aspect_sentiment_summary": local_aspect_sentiment_summary,
        },

        "explanations": explanations,
        "warnings": warnings,
        "product_insight": product_insights,
    }


def analyze_review(text, tokenizer=None, model=None, device=None):
    result = analyze_review_for_ui(
        text=text,
        rating=None,
        tokenizer=tokenizer,
        model=model,
        device=device,
    )

    if not result.get("success"):
        return result

    return {
        "text": result["input"]["text"],
        "rule_categories": [
            item["category"]
            for item in result["categories"]["rule_categories"]
        ],
        "rule_match_details": result["categories"]["rule_match_details"],
        "bert_top_predictions": [
            (item["category"], item["probability"])
            for item in result["categories"]["bert_top_predictions"]
        ],
        "final_categories": [
            item["category"]
            for item in result["categories"]["final_categories"]
        ],
        "decision_details": result["categories"]["decision_details"],
    }


def main():
    tokenizer, model, device = load_model()

    sample_reviews = [
        "oyun güzel ama çok reklam var ve sürekli kasıyor",
        "reklamdaki oyunla alakası yok bambaşka bir şey çıkıyor",
        "oyun açılmıyor sürekli hata veriyor",
        "çok güzel eğlenceli bir oyun herkese tavsiye ederim",
        "bölümler çok zor hamle yetmiyor",
        "kart vermiyor hep aynı kart çıkıyor",
    ]

    for review in sample_reviews:
        result = analyze_review_for_ui(
            text=review,
            rating=None,
            tokenizer=tokenizer,
            model=model,
            device=device,
        )

        print("\n" + "=" * 80)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()