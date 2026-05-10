from src.preprocess_reviews import (
    clean_text,
    reduce_repeated_chars,
    normalize_tokens,
    is_probably_turkish,
    is_meaningful_short_comment
)

def test_reduce_repeated_chars():
    assert reduce_repeated_chars("Çooook güzel!!!") == "Çook güzel!!"
    assert reduce_repeated_chars("reklammmmm") == "reklamm"
    assert reduce_repeated_chars("normal") == "normal"

def test_normalize_tokens():
    assert normalize_tokens("guzel oyun") == "güzel oyun"
    assert normalize_tokens("kasiyor") == "kasıyor"
    assert normalize_tokens("bilinmeyenkelime") == "bilinmeyenkelime"

def test_clean_text():
    # Empty or emoji-only text should become empty or non-analyzable.
    assert clean_text("") == ""
    assert clean_text("😊😊😊") == ""
    # "Çooook guzel!!!" should normalize repeated characters.
    assert clean_text("Çooook guzel!!! @kullanici") == "çook güzel kullanici"
    assert clean_text("http://example.com guzel") == "güzel"

def test_is_probably_turkish():
    assert is_probably_turkish("Bu oyun çok güzel ve harika.") is True
    assert is_probably_turkish("Good game bro") is False
    assert is_probably_turkish("çok") is True # Hint word
    assert is_probably_turkish("ş") is True # Turkish char

def test_is_meaningful_short_comment():
    assert is_meaningful_short_comment("kasıyor") is True
    assert is_meaningful_short_comment("harika") is True
    assert is_meaningful_short_comment("evet") is False
    assert is_meaningful_short_comment("oyun kasıyor") is True
