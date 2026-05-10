from src.analyze_categories import (
    exact_match,
    regex_match,
    fuzzy_match,
    near_match,
    find_categories_with_details,
)

def test_exact_match():
    assert exact_match("çok reklam var", ["reklam"])[0] is True
    assert exact_match("güzel oyun", ["reklam"])[0] is False

def test_regex_match():
    assert regex_match("5 yıldız", [r"\b\d+\s*yıldız\b"])[0] is True
    assert regex_match("beş yıldız", [r"\b\d+\s*yıldız\b"])[0] is False

def test_fuzzy_match():
    # Threshold is 88
    assert fuzzy_match("performas", ["performans"])[0] is True
    assert fuzzy_match("perfromans", ["performans"])[0] is True
    assert fuzzy_match("alakasız", ["mükemmel"])[0] is False

def test_near_match():
    rules = [{"terms": ["bölüm", "zor"], "max_distance": 4}]
    assert near_match("bu bölüm gerçekten çok zor", rules)[0] is True
    assert near_match("bölüm güzel ama oyunun sonları biraz zor", rules)[0] is False

def test_find_categories_with_details():
    # "çok reklam var" should match reklam
    cats, details = find_categories_with_details("çok reklam var")
    assert "reklam" in cats

    # "reklam yok oyun güzel" should still match reklam as an aspect.
    cats, details = find_categories_with_details("reklam yok oyun güzel")
    assert "reklam" in cats
    assert "olumlu_deneyim" in cats

    # "oyun çok güzel ama siyah ekran var" should match olumlu_deneyim and cihaz_goruntu_sorunu
    cats, details = find_categories_with_details("oyun çok güzel ama siyah ekran var")
    assert "olumlu_deneyim" in cats
    assert "cihaz_goruntu_sorunu" in cats

    # "çok güzel ama para harcamak zorunda kalıyorum" should not falsely match zorluk_level_design
    cats, details = find_categories_with_details("çok güzel ama para harcamak zorunda kalıyorum")
    assert "zorluk_level_design" not in cats
    assert "olumlu_deneyim" in cats
    assert "odeme_satin_alma_ekonomi" in cats

def test_regression_categories():
    # advertisement detection should not break
    assert "reklam" in find_categories_with_details("her el sonu reklam çıkıyor")[0]
    
    # loading/opening problem detection should not break
    assert "yukleme_acilis_sorunu" in find_categories_with_details("oyun açılmıyor siyah ekranda kalıyor")[0]

    # performance/kasma detection should not break
    assert "performans_donma_kasma" in find_categories_with_details("oyun çok fena kasıyor oynanmıyor")[0]

    # payment/economy detection should not break
    assert "odeme_satin_alma_ekonomi" in find_categories_with_details("her şey parayla satılıyor")[0]

    # general positive and general negative experience detection should still work
    assert "olumlu_deneyim" in find_categories_with_details("mükemmel bir oyun harika")[0]
    assert "genel_negatif_deneyim" in find_categories_with_details("hayatımda oynadığım en iğrenç oyun berbat")[0]
