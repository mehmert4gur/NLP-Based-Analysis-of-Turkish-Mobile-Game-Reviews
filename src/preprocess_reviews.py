import pandas as pd
import re
from pathlib import Path

RAW_PATH = Path("data/raw/yerel_oyun_yorumlari.xlsx")
PROCESSED_PATH = Path("data/processed/temiz_yorumlar.xlsx")

PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)


NORMALIZATION_MAP = {
    "guzel": "güzel",
    "gzl": "güzel",
    "güze": "güzel",
    "mukemmel": "mükemmel",
    "super": "süper",
    "süperr": "süper",
    "berbattt": "berbat",
    "kotu": "kötü",
    "cok": "çok",
    "coook": "çok",
    "çokkk": "çok",

    "kasiyo": "kasıyor",
    "kasiyor": "kasıyor",

    "donuyo": "donuyor",
    "donuyorrr": "donuyor",

    "acilmiyor": "açılmıyor",
    "açilmiyor": "açılmıyor",

    "reklm": "reklam",
    "reklem": "reklam",
    "reklamm": "reklam",

    "tanitim": "tanıtım",

    "internetli": "internet",

    "offline": "çevrimdışı",
    "online": "çevrimiçi",

    # yeni eklenenler
    "zorlastirilmis": "zorlaştırılmış",
    "zorlasti": "zorlaştı",
    "sacma": "saçma",

    "silecegim": "sileceğim",
    "silecem": "sileceğim",

    "haketmiyorsunuz": "hak etmiyorsunuz",

    "oynatmiyorlar": "oynatmıyorlar",

    "gosterdikleri": "gösterdikleri",
    "gorsel": "görsel",

    "kumara": "kumar",
}


TURKISH_HINT_WORDS = {
    "bir", "çok", "oyun", "güzel", "kötü", "reklam", "para",
    "level", "bölüm", "açılmıyor", "kasıyor", "donuyor", "harika",
    "berbat", "süper", "mükemmel", "neden", "ama", "değil",
    "var", "yok", "hep", "çok", "az", "zor", "kolay",
    "hile", "hileli", "kumar", "saçma"
}


SHORT_MEANINGFUL_WORDS = {
    "güzel", "harika", "mükemmel", "süper", "iyi",
    "kötü", "berbat", "rezalet", "reklam",
    "kasıyor", "donuyor", "açılmıyor", "zor", "kolay",
    "sıkıcı", "bug", "hata", "hile", "hileli",
    "saçma", "kumar"
}


def reduce_repeated_chars(text: str) -> str:
    return re.sub(r"(.)\1{2,}", r"\1\1", text)


def normalize_tokens(text: str) -> str:
    tokens = text.split()
    normalized_tokens = []

    for token in tokens:
        token = NORMALIZATION_MAP.get(token, token)
        normalized_tokens.append(token)

    return " ".join(normalized_tokens)


def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = re.sub(r"http\S+|www\.\S+", " ", text)

    text = re.sub(r"[@#]", " ", text)

    text = re.sub(r"[^a-zA-ZğüşöçıİĞÜŞÖÇ0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    text = reduce_repeated_chars(text)

    text = normalize_tokens(text)

    return text


def is_probably_turkish(text: str) -> bool:
    if not text:
        return False

    tokens = text.split()

    if not tokens:
        return False

    has_turkish_char = bool(re.search(r"[ğüşöçıİĞÜŞÖÇ]", text))

    hint_count = sum(1 for token in tokens if token in TURKISH_HINT_WORDS)

    if len(tokens) <= 2:
        return has_turkish_char or hint_count >= 1

    return has_turkish_char or hint_count >= 1


def is_meaningful_short_comment(text: str) -> bool:
    tokens = text.split()

    if len(tokens) == 1:
        return tokens[0] in SHORT_MEANINGFUL_WORDS

    if len(tokens) == 2:
        return any(token in SHORT_MEANINGFUL_WORDS for token in tokens)

    return False


def preprocess():
    df = pd.read_excel(RAW_PATH)

    print("İlk veri boyutu:", len(df))

    df = df.dropna(subset=["content"])
    df = df[df["content"].astype(str).str.strip() != ""]

    if "review_id" in df.columns:
        df = df.drop_duplicates(subset=["review_id"])
    else:
        df = df.drop_duplicates(subset=["content"])

    df["original_text"] = df["content"].astype(str)
    df["clean_text"] = df["content"].apply(clean_text)

    df["is_empty_after_cleaning"] = df["clean_text"].str.strip() == ""
    df["word_count"] = df["clean_text"].apply(lambda x: len(str(x).split()))
    df["is_short"] = df["word_count"] < 3

    df["is_probably_turkish"] = df["clean_text"].apply(is_probably_turkish)
    df["is_meaningful_short"] = df["clean_text"].apply(is_meaningful_short_comment)

    df["is_analyzable"] = (
        (~df["is_empty_after_cleaning"]) &
        (df["is_probably_turkish"]) &
        (
            (df["word_count"] >= 3) |
            (df["is_meaningful_short"])
        )
    )

    if "review_created_at" in df.columns:
        df["review_created_at"] = pd.to_datetime(
            df["review_created_at"],
            errors="coerce"
        )

        df["year"] = df["review_created_at"].dt.year
        df["month"] = df["review_created_at"].dt.month

    df.to_excel(PROCESSED_PATH, index=False)

    print("Temizlik sonrası toplam:", len(df))
    print("Temizleme sonrası boş kalan:", df["is_empty_after_cleaning"].sum())
    print("Çok kısa yorum:", df["is_short"].sum())
    print("Anlamlı kısa yorum:", df["is_meaningful_short"].sum())
    print("Muhtemelen Türkçe:", df["is_probably_turkish"].sum())
    print("Analize uygun yorum:", df["is_analyzable"].sum())
    print("Kaydedildi:", PROCESSED_PATH)


if __name__ == "__main__":
    preprocess()