from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from analyze_categories import find_categories_with_details


MODEL_DIR = Path("outputs/models/berturk_multilabel_absa_full/best_model")

MAX_LENGTH = 128
BERT_THRESHOLD = 0.35
HIGH_CONFIDENCE_THRESHOLD = 0.60


def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    return tokenizer, model, device


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

    for category, probability in bert_probs.items():
        if probability >= HIGH_CONFIDENCE_THRESHOLD:
            final_categories.add(category)
            decision_details.append({
                "category": category,
                "source": "bert_high_confidence",
                "probability": round(probability, 4),
            })

        elif probability >= BERT_THRESHOLD and category in rule_categories:
            final_categories.add(category)
            decision_details.append({
                "category": category,
                "source": "rule_and_bert_agree",
                "probability": round(probability, 4),
            })

    for category in rule_categories:
        decision_details.append({
            "category": category,
            "source": "rule_based",
            "probability": round(bert_probs.get(category, 0), 4),
        })

    return sorted(final_categories), decision_details


def analyze_review(text, tokenizer, model, device):
    rule_categories, rule_match_details = find_categories_with_details(text)

    bert_probs = predict_berturk_categories(
        text=text,
        tokenizer=tokenizer,
        model=model,
        device=device,
    )

    final_categories, decision_details = hybrid_decision(
        rule_categories=rule_categories,
        bert_probs=bert_probs,
    )

    top_bert = sorted(
        bert_probs.items(),
        key=lambda x: x[1],
        reverse=True,
    )[:8]

    return {
        "text": text,
        "rule_categories": rule_categories,
        "rule_match_details": rule_match_details,
        "bert_top_predictions": top_bert,
        "final_categories": final_categories,
        "decision_details": decision_details,
    }


def print_result(result):
    print("\n" + "=" * 80)
    print("Yorum:")
    print(result["text"])

    print("\nRule-based kategoriler:")
    if result["rule_categories"]:
        for category in result["rule_categories"]:
            print(f"- {category}")
    else:
        print("- yok")

    print("\nBERTürk top tahminler:")
    for label, prob in result["bert_top_predictions"]:
        print(f"- {label}: {prob:.3f}")

    print("\nFinal hybrid kategoriler:")
    if result["final_categories"]:
        for category in result["final_categories"]:
            print(f"- {category}")
    else:
        print("- yok")

    print("\nKarar detayları:")
    for detail in result["decision_details"]:
        print(
            f"- {detail['category']} | "
            f"{detail['source']} | "
            f"prob={detail['probability']}"
        )


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
        result = analyze_review(
            text=review,
            tokenizer=tokenizer,
            model=model,
            device=device,
        )

        print_result(result)


if __name__ == "__main__":
    main()