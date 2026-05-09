# src/category_rules.py

CATEGORY_RULES = {
    "rating_manipulation": {
        "keywords": [
            "5 yıldız verdim", "beş yıldız verdim",
            "yorumum üstte gözüksün", "ön plana çıksın",
            "sırf gözüksün", "başta gözüksün",
            "görünsün diye", "üstte gözüksün"
        ],
        "regex": [
            r"(5|beş)\s*yıldız.*(gözüksün|görünsün|üste|üstte)",
            r"yorum.*(üstte|üste|gözüksün|görünsün)"
        ],
        "fuzzy": []
    },

    "reklam": {
        "keywords": [
            "reklam", "reklamlar", "reklam çıkıyor", "çok reklam",
            "reklam tuzağı", "uzun reklam", "reklam süresi",
            "her bölümde reklam", "ads", "ad not ready", "video reklam"
        ],
        "regex": [
            r"her\s+(oyun|bölüm|level|seviye).*reklam",
            r"(oyundan|oyun).*çok.*reklam",
            r"sürekli.*reklam",
            r"reklam.*(çok|fazla|uzun|bitmiyor|çıkıyor)",
            r"(video|tanıtım).*reklam"
        ],
        "fuzzy": [
            "reklam", "reklem", "reklm", "reklamm"
        ]
    },

    "yaniltici_reklam_tanitim": {
        "keywords": [
            "reklamla oyunun alakası yok", "reklamla alakası yok",
            "reklamdaki gibi değil", "reklamdakiyle alakası yok",
            "reklamdaki oyun yok", "reklam başka oyun başka",
            "reklam farklı oyun farklı", "tanıtımdaki gibi değil",
            "tanıtıldığı gibi değil", "görseldeki oyun yok",
            "görselle alakası yok", "fotoğraflardaki gibi değil",
            "videodaki gibi değil", "kandırmaca", "aldatıcı",
            "dolandırıcılık", "hayal kırıklığı", "gösterilen oyun"
        ],
        "regex": [
            r"reklam.*(alakası yok|farklı|başka|gibi değil)",
            r"tanıtım.*(alakası yok|farklı|başka|gibi değil)",
            r"görsel.*(alakası yok|oyun yok|çıkmadı)",
            r"video.*(alakası yok|gibi değil)",
            r"gösterilen.*oyun.*(yok|değil)",
            r"(kandırmaca|aldatıcı|dolandırıcılık)"
        ],
        "fuzzy": [
            "aldatıcı", "kandırmaca", "dolandırıcılık"
        ]
    },

    "guncelleme_sorunu": {
        "keywords": [
            "güncelleyemiyorum", "güncellenmiyor",
            "güncelleme yok", "güncelleme gelmiyor",
            "güncelleme yapamıyorum", "son güncelleme",
            "güncellemeden sonra", "güncelleme geç geliyor"
        ],
        "regex": [
            r"güncelleme.*(yok|gelmiyor|yapamıyorum|sorun|hata)",
            r"güncellemeden sonra.*(bozuldu|açılmıyor|kasıyor|hata|donuyor)",
            r"son güncelleme.*(kötü|bozdu|hata|sorun)"
        ],
        "fuzzy": [
            "güncellenmiyor", "güncelleyemiyorum"
        ]
    },

    "yeni_bolum_icerik_eksikligi": {
        "keywords": [
            "yeni bölüm gelmiyor", "devamı gelmiyor", "oyun bitti",
            "seviye kalmadı", "bölüm kalmadı", "arena da bitti",
            "yeni seviyeler", "bölümleri bitirdim", "son bölüm",
            "devamını bekliyorum", "çok az bölüm", "seviyeleri az"
        ],
        "regex": [
            r"yeni\s+(bölüm|seviye|level).*gelmiyor",
            r"(bölüm|seviye|level).*kalmadı",
            r"(oyun|bölümler|seviyeler).*bitti",
            r"devamı.*gelmiyor",
            r"ne zaman.*(gelecek|gelir)",
            r"(çok az|az).*bölüm"
        ],
        "fuzzy": []
    },

    "cihaz_goruntu_sorunu": {
        "keywords": [
            "siyah ekran", "siyah pikseller", "görüntü bozuk",
            "grafikleri bozuk", "yazı okunmuyor", "simsiyah karışık bir ekran",
            "siyah karışık ekran", "telefonumda çalışmadı",
            "uyumlu değil", "yüklenemez", "telefon ısınıyor",
            "telefon kitleniyor", "şarj yiyor"
        ],
        "regex": [
            r"siyah.*ekran",
            r"görüntü.*bozuk",
            r"grafik.*bozuk",
            r"telefon.*(ısınıyor|kitleniyor|çalışmadı)",
            r"(cihaz|telefon|tablet).*(uyumlu değil|çalışmadı|desteklemiyor)",
            r"şarj.*(yiyor|bitiriyor|tüketiyor)"
        ],
        "fuzzy": [
            "çözünürlük"
        ]
    },

    "yukleme_acilis_sorunu": {
        "keywords": [
            "yüklenmiyor", "yüklenme kısmında kalıyor", "açılmıyor",
            "açılmadı", "oyuna giremiyorum", "giriş yapamıyorum",
            "oyuna giriş yapamıyorum", "oyun açılmıyor", "oyun açılmadı",
            "indirilmiyor", "yüklemiyor", "60 da kalıyor",
            "hata veriyor", "teknik hata", "oyuna girmeden atıyor",
            "uygulama çalışmıyor", "uygulamayı indiremedim"
        ],
        "regex": [
            r"oyun.*açılmıyor",
            r"oyuna.*giremiyorum",
            r"giriş.*yapamıyorum",
            r"yüklenme.*kalıyor",
            r"(60|100).*kalıyor",
            r"uygulama.*çalışmıyor",
            r"(indirilmiyor|yüklenmiyor|açılmadı)"
        ],
        "fuzzy": [
            "açılmıyor", "acilmiyor", "yüklenmiyor", "yuklenmiyor",
            "giremiyorum", "indirilmiyor"
        ]
    },

    "performans_donma_kasma": {
        "keywords": [
            "kasıyor", "donuyor", "dondu", "donma",
            "takılıyor", "çok yavaş", "geç açılıyor",
            "yüklenmesi uzun", "kasma oluyor",
            "scene transitions are too slow", "3 fps",
            "aşırı kasıyor", "oyun çok geç açılıyor",
            "şarj tüketiyor", "ısındırıyor"
        ],
        "regex": [
            r"(çok|aşırı|fazla)?.*kasıyor",
            r"oyun.*donuyor",
            r"çok.*yavaş",
            r"geç.*açılıyor",
            r"telefon.*ısınıyor",
            r"şarj.*(yiyor|tüketiyor|bitiriyor)",
            r"\d+\s*fps"
        ],
        "fuzzy": [
            "kasıyor", "kasiyor", "donuyor", "takılıyor", "takiliyor"
        ]
    },

    "crash_hata_bug": {
        "keywords": [
            "bug", "hatalı", "hata oluşması", "bölümde hata",
            "levelde hata", "kendi kendine çıkıyor", "oyundan atıyor",
            "kapanıyor", "çöküyor", "bozuk oyun", "dokunmatik algılamıyor",
            "tuş yok", "seçenek yok", "ses yok", "titreşim yok"
        ],
        "regex": [
            r"oyundan.*atıyor",
            r"kendi kendine.*(çıkıyor|kapanıyor)",
            r"(hata|bug).*var",
            r"(dokunmatik|tuş|ses|titreşim).*(yok|çalışmıyor|algılamıyor)",
            r"oyun.*(çöküyor|kapanıyor)"
        ],
        "fuzzy": [
            "çöküyor", "kapanıyor", "algılamıyor"
        ]
    },

    "zorluk_level_design": {
        "keywords": [
            "zorlaşıyor", "zorlaştır", "geçemiyorum", "geçilmiyor",
            "geçirmiyor", "ilerleyemiyorum", "takıldım", "aynı bölüm",
            "hep aynı", "aynı leveller", "sinir bozucu", "sinir krizi",
            "çok kolay", "fazla kolay", "bölümler çok kolay",
            "sorular çok kolay", "level design"
        ],
        "regex": [
            r"(çok|fazla|aşırı).*zor",
            r"(çok|fazla|aşırı).*kolay",
            r"(aynı|hep aynı).*(bölüm|level|seviye)",
            r"(geçemiyorum|geçilmiyor|ilerleyemiyorum)",
            r"(sıkıcı|bıktım).*",
            r"sinir.*(bozucu|krizi)",
            r"(bölüm|level|seviye).*(zor|kolay|tekrar|aynı)"
        ],
        "fuzzy": [
            "geçemiyorum", "imkansız"
        ]
    },

    "can_hamle_hak_sure": {
        "keywords": [
            "can hakkı", "5 can", "sınırsız can", "can dolma",
            "bekleme süresi", "hamle sayısı", "hareketler yetmiyor",
            "süre sınırı", "zaman çok kısa", "ek süre",
            "15 dakika süre", "her levelde mola"
        ],
        "regex": [
            r"can.*(dolmuyor|az|yetmiyor|bekleme|bitti)",
            r"hamle.*(az|yetmiyor|sayısı|bitti)",
            r"süre.*(az|kısa|yetmiyor|bitti)",
            r"zaman.*çok kısa",
            r"hak.*(az|yetmiyor|bitti)"
        ],
        "fuzzy": []
    },

    "odeme_satin_alma_ekonomi": {
        "keywords": [
            "satın alma", "satın almaya", "ücretlendirme", "ücretli",
            "pahalı", "ticarethane", "kredi kartı",
            "almaya zorluyor", "satın almaya zorluyor",
            "ödeme yap", "premium", "ücret ödemeden",
            "iade", "geri ödeme", "para iadesi"
        ],
        "regex": [
            r"para.*(verdim|çekildi|iade|gelmedi|aldı)",
            r"satın.*(aldım|alma|almaya|alın)",
            r"(ücret|ödeme|premium|kredi kartı)",
            r"(coin|altın|jeton).*(az|gelmedi|pahalı|yetmiyor)",
            r"almaya.*zorluyor"
        ],
        "fuzzy": [
            "premium", "iade"
        ]
    },

    "odul_bonus_ipucu": {
        "keywords": [
            "bonus", "ödül", "hediye", "sandık", "çark",
            "güçlendirici", "ışık top", "roket", "bomba",
            "kazandıklarını vermedi", "hediyeleri azalttılar",
            "ipucu", "ampul", "joker"
        ],
        "regex": [
            r"(ödül|bonus|hediye).*(vermiyor|az|gelmedi|alamadım)",
            r"(sandık|çark|joker|ipucu)",
            r"kazandıklarını.*vermedi"
        ],
        "fuzzy": [
            "joker", "ipucu"
        ]
    },

    "kart_koleksiyon": {
        "keywords": [
            "mor kart", "sarı kart", "gümüş kart",
            "eksik kart", "aynı kart", "kart çıkmıyor"
        ],
        "regex": [
            r"kart.*(çıkmıyor|eksik|aynı|gelmiyor)",
            r"(mor|sarı|gümüş).*kart",
            r"koleksiyon.*(eksik|tamamlanmıyor)"
        ],
        "fuzzy": []
    },

    "hile_algoritma_adalet": {
        "keywords": [
            "hile", "algoritma", "kasıtlı", "bilerek",
            "rastgele değil", "oyun isterse", "oyun seni yönetiyor",
            "kaybettiriyor", "kurmaca", "adaletsiz", "haksızlık",
            "sahtekarlık", "izin vermiyor", "oynatmıyor",
            "kafana göre", "geçme ihtimali yok",
            "kaybeden ben oluyorum", "puanlarım gelmiyor",
            "oyun bizimle oynuyor"
        ],
        "regex": [
            r"(hile|algoritma|sahtekarlık|haksızlık|adaletsiz)",
            r"oyun.*(kaybettiriyor|yönetiyor|izin vermiyor|oynatmıyor)",
            r"kafana göre",
            r"rastgele değil",
            r"bilerek.*(kaybettiriyor|vermiyor)"
        ],
        "fuzzy": [
            "adaletsiz", "haksızlık", "sahtekarlık"
        ]
    },

    "destek_iletisim": {
        "keywords": [
            "yardımcı olur musunuz", "iletişime geçemiyorum",
            "cevap vermiyor", "geri dönüş", "sorun bildir",
            "dikkate alınırsa", "çözümü nedir", "düzeltebilir miyiz",
            "müşteri temsilcisi", "ulaşamıyorum", "ilgilenmiyor",
            "açıklama yapın"
        ],
        "regex": [
            r"(destek|yardım|müşteri temsilcisi).*(lütfen|istiyorum|bekliyorum)?",
            r"cevap.*vermiyor",
            r"geri dönüş.*(yok|yapılmadı|vermiyor)",
            r"iletişime.*geçemiyorum",
            r"çözümü.*nedir"
        ],
        "fuzzy": [
            "ulaşamıyorum"
        ]
    },

    "sohbet_takim_arkadas_topluluk": {
        "keywords": [
            "sohbet", "mesaj", "ban", "erişim engeli", "spam engeli",
            "takım", "grup", "lider", "arkadaşlarımı göremiyorum",
            "arkadaş listem", "puanlarını göremiyoruz",
            "istek gönderemiyorum", "konuşamıyorum", "küfür",
            "hakaret", "oyuncu davet", "chat", "kulüp"
        ],
        "regex": [
            r"(sohbet|chat|mesaj|takım|grup|kulüp)",
            r"arkadaş.*(göremiyorum|listem|ekleyemiyorum)",
            r"(ban|erişim engeli|spam engeli)",
            r"(küfür|hakaret)"
        ],
        "fuzzy": []
    },

    "hesap_kayit_ilerleme": {
        "keywords": [
            "hesabım", "facebook", "google play", "baştan başladı",
            "sıfırdan", "kaldığım yerden", "telefonuma aktardım",
            "telefon değişikliği", "format", "oyunu silmek istiyorum",
            "telefon değişti", "yeniden başlattı",
            "levelimi geri alamadım", "oyunum silindi",
            "isim değiştirme", "1 seviyeye düştüm",
            "geri attı", "geriye dönüyor", "sıfırlanma"
        ],
        "regex": [
            r"hesab.*(silindi|gitti|geri alamadım|sıfırlandı)",
            r"(baştan|sıfırdan).*başladı",
            r"level.*geri alamadım",
            r"telefon.*değişti",
            r"(facebook|google play).*(bağlan|giriş)",
            r"ilerleme.*(gitti|silindi|kayboldu)"
        ],
        "fuzzy": [
            "sıfırlandı"
        ]
    },

    "internet_cevrimdisi": {
        "keywords": [
            "internetsiz", "çevrimdışı", "çevrim dışı",
            "internet yokken", "internet kapalıyken",
            "internet bağlantısız", "internet olmadan oynanmıyor",
            "internetsiz oynanmıyor", "internetsiz oynayamıyoruz"
        ],
        "regex": [
            r"internet.*(yok|olmadan|kapalı|çekmiyor|istemesin|bağlantı)",
            r"internetsiz.*(oynanmıyor|oynayamıyorum)",
            r"çevrim\s*dışı",
            r"wifi.*(yok|bağlanmıyor|çekmiyor)"
        ],
        "fuzzy": [
            "internetsiz", "çevrimdışı"
        ]
    },

    "gizlilik_guvenlik_izin": {
        "keywords": [
            "gizlilik", "sözleşme", "kullanım koşulları",
            "kabul etmek zorundayım", "kişisel bilgiler", "rehber",
            "e posta", "ajanlık", "casusluk", "izin onay",
            "bildirim izni", "güvenli değil", "kimlik",
            "finansal bilgiler"
        ],
        "regex": [
            r"(gizlilik|sözleşme|kullanım koşulları)",
            r"(kişisel|finansal).*bilgi",
            r"(rehber|kimlik|e posta).*izin",
            r"güvenli değil"
        ],
        "fuzzy": []
    },

    "dil_lokalizasyon": {
        "keywords": [
            "türkçe değil", "ingilizceye geçiyor",
            "yarı ingilizce", "sorular ingilizce",
            "türkçe olmuyor", "dil desteği"
        ],
        "regex": [
            r"türkçe.*(değil|olmuyor|yok)",
            r"ingilizce.*(geçiyor|sorular|oluyor|kaldı)",
            r"dil.*(desteği|sorunu|yok|değişmiyor)",
            r"çeviri.*(kötü|hatalı|yok)"
        ],
        "fuzzy": []
    },

    "uygunsuz_icerik_yas": {
        "keywords": [
            "çocuklar için uygun değil", "küçük çocuklar",
            "yaş sınırı", "uygunsuz", "cinsel",
            "sapık", "kötü örnek", "çocuklara kötü",
            "şiddet", "aldatma"
        ],
        "regex": [
            r"çocuk.*(uygun değil|kötü)",
            r"(yaş sınırı|uygunsuz|cinsel|şiddet|aldatma)",
            r"kötü örnek"
        ],
        "fuzzy": []
    },

    "egitici_bilissel_fayda": {
        "keywords": [
            "beyin geliştirme", "kelime haznesi",
            "kelime öğren", "karar verme",
            "eğitici", "öğretici", "hafıza",
            "zeka geliştiriyor", "zihin geliştiriyor",
            "mantık", "bulmaca"
        ],
        "regex": [
            r"(beyin|zeka|zihin|hafıza).*geliştir",
            r"(eğitici|öğretici|bilgi|mantık|bulmaca)",
            r"kelime.*(öğren|haznesi)"
        ],
        "fuzzy": []
    },

    "olumlu_deneyim": {
        "keywords": [
            "çok güzel", "güzel oyun", "harika", "mükemmel",
            "muhteşem", "süper", "keyifli", "eğlenceli",
            "sürükleyici", "rahatlatıcı", "bağımlılık",
            "bağımlısı", "tavsiye ederim", "öneririm",
            "beğendim", "bayıldım", "kafa dağıtmak",
            "stres at", "başarılı", "on numara", "10 numara",
            "kaliteli", "zevkli", "sarıyor", "çok iyi",
            "efsane", "müq", "mük", "perfect", "excellent",
            "iyi oyun", "ellerinize sağlık", "severek oynuyorum",
            "favori oyunum", "şahane"
        ],
        "regex": [
            r"(çok|aşırı|gayet).*(güzel|iyi|harika|mükemmel|süper)",
            r"tavsiye.*ederim",
            r"(beğendim|bayıldım|efsane|şahane)",
            r"severek.*oynuyorum",
            r"ellerinize sağlık"
        ],
        "fuzzy": [
            "güzel", "guzel", "harika", "mükemmel", "mukemmel", "efsane"
        ]
    },

    "genel_negatif_deneyim": {
        "keywords": [
            "berbat", "rezalet", "çok kötü", "saçma",
            "beğenmedim", "hiç iyi değil", "boş oyun",
            "zaman kaybı", "sildim", "sileceğim", "oynamayın",
            "indirmeyin", "tavsiye etmiyorum", "nefret", "lanet",
            "çekilmez", "oynayası gelmiyor", "benlik değil",
            "sarmıyor", "bomboş bir oyun", "zamanınıza yazık",
            "5 kuruş etmiyor", "yüklemeye değmez", "başarısız",
            "siz oyun yapmayın", "kıymetsiz", "gereksiz",
            "çöp", "kötü oyun"
        ],
        "regex": [
            r"(çok|aşırı|fazla).*(kötü|berbat|rezalet|saçma)",
            r"zaman.*kaybı",
            r"(oynamayın|indirmeyin|sildim|sileceğim)",
            r"tavsiye.*etmiyorum",
            r"(çöp|gereksiz|boş oyun|bomboş)"
        ],
        "fuzzy": [
            "berbat", "rezalet", "gereksiz"
        ]
    },

    "gelistirme_onerisi": {
        "keywords": [
            "olmalı", "eklenmeli", "getirilsin", "düzeltilmeli",
            "düzeltin", "daha iyi olur", "çözüm bulun",
            "artırılsın", "kısaltılsın", "lütfen",
            "rica ediyorum", "yenilik", "değiştirme yapılabilmeli",
            "daha fazlası olabilir", "devam ettirebilirsiniz",
            "devamını yaparsanız", "farklı oyunlar olsa",
            "nasıl oynanır açıklaması", "eklenirse",
            "olsaydı", "değiştirilebilir", "geliştirilebilir"
        ],
        "regex": [
            r"(eklenmeli|olmalı|getirilsin|düzeltilmeli)",
            r"(düzeltin|çözüm bulun|lütfen)",
            r"daha iyi olur",
            r".*olsa.*iyi olur",
            r"(geliştirilebilir|değiştirilebilir)"
        ],
        "fuzzy": []
    },

    "spam_anlamsiz": {
        "keywords": [
            "dudndjd", "hzhhjd", "ndkdj", "full film indir",
            "ak partinin oy oranı", "staff bu arada", "usta yavuz",
            "messi", "anne kakam", "ı ı ı", "ok borveg"
        ],
        "regex": [
            r"^[a-zğüşöçı]{1,2}$",
            r"(.)\1{5,}",
            r"^[a-zğüşöçı\s]{0,3}$",
            r"\b(full film indir|messi|ak parti)\b"
        ],
        "fuzzy": []
    }
}