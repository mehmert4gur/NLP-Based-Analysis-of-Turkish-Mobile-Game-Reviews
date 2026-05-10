import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_DIR = Path("outputs/models/berturk_multilabel_absa_pilot/pilot_model")
THRESHOLD = 0.35
TOP_K = 8


SAMPLE_TEXTS = [
    "oyun güzel ama çok reklam var ve sürekli kasıyor",
    "reklamdaki oyunla alakası yok bambaşka bir şey çıkıyor",
    "oyun açılmıyor sürekli hata veriyor",
    "çok güzel eğlenceli bir oyun herkese tavsiye ederim",
    "bölümler çok zor hamle yetmiyor",
    "kart vermiyor hep aynı kart çıkıyor",
]


def predict_texts(texts):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    model.eval()

    id2label = model.config.id2label

    for text in texts:
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=96,
        )

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits[0]
            probs = torch.sigmoid(logits)

        scored_labels = [
            (id2label[i], float(probs[i]))
            for i in range(len(probs))
        ]

        scored_labels = sorted(
            scored_labels,
            key=lambda x: x[1],
            reverse=True,
        )

        predicted = [
            (label, score)
            for label, score in scored_labels
            if score >= THRESHOLD
        ]

        print("\n" + "=" * 80)
        print("Yorum:")
        print(text)

        print("\nTahmin edilen kategoriler:")
        if predicted:
            for label, score in predicted:
                print(f"- {label}: {score:.3f}")
        else:
            print("- Eşik üstü kategori yok")

        print(f"\nEn yüksek {TOP_K} olasılık:")
        for label, score in scored_labels[:TOP_K]:
            print(f"- {label}: {score:.3f}")


if __name__ == "__main__":
    predict_texts(SAMPLE_TEXTS)