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
            "reklam", "reklamlar", "reklamı", "reklamları",
            "çok reklam", "reklam çıkıyor", "reklam yok",
            "reklamsız", "reklam olmayışı", "reklam tuzağı",
            "uzun reklam", "reklam süresi", "her oyuna reklam",
            "her bölümde reklam", "ads", "ad not ready",
            "tanıtım", "video reklam"
        ],
        "regex": [
            r"her\s+(oyun|bölüm|level|seviye).*reklam",
            r"(oyundan|oyun).*çok.*reklam",
            r"sürekli.*reklam",
            r"reklam.*(çok|fazla|uzun|bitmiyor)",
            r"(reklam|video).*çıkıyor",
            r"(reklamsız|reklam yok)"
        ],
        "fuzzy": [
            "reklam", "reklem", "reklm", "reklamm", "tanitim", "tanıtım"
        ]
    },

    "yaniltici_reklam_tanitim": {
        "keywords": [
            "reklamla oyunun alakası yok", "reklamla alakası yok",
            "reklamdaki gibi değil", "reklamdakiyle alakası yok",
            "reklamdaki oyun yok", "reklamdaki bölümler yok",
            "reklam başka oyun başka", "reklam farklı oyun farklı",
            "reklamlarda gösterilen oyun", "tanıtımdaki gibi değil",
            "tanıtıldığı gibi değil", "görseldeki oyun yok",
            "görselle alakası yok", "fotoğraflardaki gibi değil",
            "videodaki gibi değil", "kandırmaca", "aldatıcı",
            "dolandırıcılık", "hayal kırıklığı", "alakası yok",
            "gösterilen oyun", "istediğim gibi değildi",
            "oyun içeriği böyle değildi", "tanıtıldığı gibi bir oyun değil",
            "görseldeki oyunlar çıkmadı", "oyun reklam"
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
            "aldatıcı", "kandırmaca", "dolandırıcılık", "tanıtım"
        ]
    },

    "guncelleme_sorunu": {
        "keywords": [
            "güncelleme", "güncelleyemiyorum", "güncellenmiyor",
            "güncelleme yok", "güncelleme gelmiyor",
            "güncelleme yapamıyorum", "son güncelleme",
            "güncellemeden sonra", "güncelleme geç geliyor",
            "her hafta güncelleme"
        ],
        "regex": [
            r"güncelleme.*(yok|gelmiyor|yapamıyorum|sorun|hata)",
            r"güncellemeden sonra.*(bozuldu|açılmıyor|kasıyor|hata)",
            r"son güncelleme.*(kötü|bozdu|hata)"
        ],
        "fuzzy": [
            "güncelleme", "guncelleme", "güncellenmiyor"
        ]
    },

    "yeni_bolum_icerik_eksikligi": {
        "keywords": [
            "yeni bölüm", "yeni bölümler", "yeni bölüm gelmiyor",
            "ne zaman gelecek", "devamı gelmiyor", "oyun bitti",
            "seviye kalmadı", "bölüm kalmadı", "arena da bitti",
            "şampiyonlar ligi", "efsane arena", "yeni seviyeler",
            "bölümleri bitirdim", "son bölüm", "devamını bekliyorum",
            "çok az bölüm", "seviyeleri az", "yeni macera"
        ],
        "regex": [
            r"yeni\s+(bölüm|seviye|level).*gelmiyor",
            r"(bölüm|seviye|level).*kalmadı",
            r"(oyun|bölümler|seviyeler).*bitti",
            r"devamı.*gelmiyor",
            r"ne zaman.*gelecek"
        ],
        "fuzzy": [
            "bölüm", "seviye", "level"
        ]
    },

    "cihaz_goruntu_sorunu": {
        "keywords": [
            "siyah ekran", "siyah pikseller", "piksel", "görüntü bozuk",
            "grafikleri bozuk", "yazı okunmuyor", "gözükmüyor",
            "simsiyah karışık bir ekran", "siyah karışık ekran",
            "telefonumda çalışmadı", "tablet", "android", "honor",
            "kaplama", "çözünürlük", "şarj yiyor", "telefon ısınıyor",
            "telefon kitleniyor", "cihaz", "uyumlu değil", "yüklenemez"
        ],
        "regex": [
            r"siyah.*ekran",
            r"görüntü.*bozuk",
            r"grafik.*bozuk",
            r"telefon.*(ısınıyor|kitleniyor|çalışmadı)",
            r"(cihaz|telefon|tablet).*(uyumlu değil|çalışmadı)"
        ],
        "fuzzy": [
            "ekran", "piksel", "görüntü", "grafik", "çözünürlük"
        ]
    },

    "yukleme_acilis_sorunu": {
        "keywords": [
            "yüklenmiyor", "yüklenme kısmında kalıyor", "açılmıyor",
            "açılmadı", "oyuna giremiyorum", "giriş yapamıyorum",
            "oyuna giriş yapamıyorum", "oyun açılmıyor", "oyun açılmadı",
            "indirilmiyor", "yüklemiyor", "60 da kalıyor",
            "100 oluyor", "hata veriyor", "teknik hata",
            "açmaya çalıştığımda", "oyuna girmeden atıyor",
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
            "kasıyor", "kasiyor", "donuyor", "dondu", "donma",
            "takılıyor", "takiliyor", "yavaş", "yavas", "çok yavaş",
            "geç açılıyor", "yüklenmesi uzun", "kasma oluyor",
            "scene transitions are too slow", "3 fps",
            "bloklar oynamıyor", "blok hareket", "aşırı kasıyor",
            "oyun çok geç açılıyor", "optimize", "ısındırıyor",
            "şarj tüketiyor"
        ],
        "regex": [
            r"(çok|aşırı|fazla)?.*kasıyor",
            r"oyun.*donuyor",
            r"çok.*yavaş",
            r"geç.*açılıyor",
            r"telefon.*ısınıyor",
            r"şarj.*(yiyor|tüketiyor)",
            r"\d+\s*fps"
        ],
        "fuzzy": [
            "kasıyor", "kasiyor", "donuyor", "takılıyor",
            "takiliyor", "yavaş", "yavas"
        ]
    },

    "crash_hata_bug": {
        "keywords": [
            "bug", "hata", "hatalı", "hata oluşması", "bölümde hata",
            "levelde hata", "geçmesi gereken bölümü geçmiyor",
            "kendi kendine çıkıyor", "oyundan atıyor", "kapanıyor",
            "çöküyor", "bozuk oyun", "dokunmatik", "algılamıyor",
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
            "hata", "bug", "çöküyor", "kapanıyor", "algılamıyor"
        ]
    },

    "zorluk_level_design": {
        "keywords": [
            "zor", "zorlaşıyor", "zorlaştır", "geçemiyorum", "geçilmiyor",
            "geçirmiyor", "ilerleyemiyorum", "takıldım", "aynı bölüm",
            "hep aynı", "aynı leveller", "tekrar", "sıkıcı", "bıktım",
            "imkansız", "sinir bozucu", "sinir krizi", "çok kolay",
            "fazla kolay", "basit", "bölümler çok kolay",
            "sorular çok kolay", "level design", "seviye", "bölüm"
        ],
        "regex": [
            r"(çok|fazla).*zor",
            r"(çok|fazla).*kolay",
            r"(aynı|hep aynı).*(bölüm|level|seviye)",
            r"(geçemiyorum|geçilmiyor|ilerleyemiyorum)",
            r"(sıkıcı|bıktım|tekrar)",
            r"sinir.*(bozucu|krizi)"
        ],
        "fuzzy": [
            "zor", "kolay", "sıkıcı", "geçemiyorum", "imkansız"
        ]
    },

    "can_hamle_hak_sure": {
        "keywords": [
            "can", "canlar", "can hakkı", "5 can", "sınırsız can",
            "can dolma", "bekleme süresi", "bekletmek", "hamle",
            "hamle sayısı", "hareketler yetmiyor", "hak", "süre",
            "süre sınırı", "zaman çok kısa", "ek süre",
            "15 dakika süre", "mola", "her levelde mola"
        ],
        "regex": [
            r"can.*(dolmuyor|az|yetmiyor|bekleme)",
            r"hamle.*(az|yetmiyor|sayısı)",
            r"süre.*(az|kısa|yetmiyor)",
            r"zaman.*çok kısa",
            r"hak.*(az|yetmiyor|bitti)"
        ],
        "fuzzy": [
            "can", "hamle", "süre", "hak"
        ]
    },

    "odeme_satin_alma_ekonomi": {
        "keywords": [
            "satın alma", "satın almaya", "ücretlendirme", "ücretli",
            "para", "altın", "coin", "jeton", "iksir", "pahalı",
            "ticarethane", "kredi kartı", "almaya zorluyor",
            "satın almaya zorluyor", "ödeme yap", "premium",
            "ücret ödemeden", "iade", "geri ödeme", "para iadesi"
        ],
        "regex": [
            r"para.*(verdim|çekildi|iade|gelmedi)",
            r"satın.*(aldım|alma|almaya)",
            r"(ücret|ödeme|premium|kredi kartı)",
            r"(coin|altın|jeton).*(az|gelmedi|pahalı)",
            r"almaya.*zorluyor"
        ],
        "fuzzy": [
            "para", "ödeme", "ücret", "premium", "iade", "coin", "jeton"
        ]
    },

    "odul_bonus_ipucu": {
        "keywords": [
            "bonus", "ödül", "hediye", "sandık", "çark", "güçlendirici",
            "ışık top", "roket", "bomba", "envanter",
            "kazandıklarını vermedi", "hediyeleri azalttılar",
            "ipucu", "ampul", "joker"
        ],
        "regex": [
            r"(ödül|bonus|hediye).*(vermiyor|az|gelmedi)",
            r"(sandık|çark|joker|ipucu)",
            r"kazandıklarını.*vermedi"
        ],
        "fuzzy": [
            "ödül", "bonus", "hediye", "joker", "ipucu"
        ]
    },

    "kart_koleksiyon": {
        "keywords": [
            "kart", "kartlar", "koleksiyon", "mor kart", "sarı kart",
            "gümüş kart", "eksik kart", "aynı kart", "kart çıkmıyor"
        ],
        "regex": [
            r"kart.*(çıkmıyor|eksik|aynı|gelmiyor)",
            r"(mor|sarı|gümüş).*kart",
            r"koleksiyon"
        ],
        "fuzzy": [
            "kart", "koleksiyon"
        ]
    },

    "hile_algoritma_adalet": {
        "keywords": [
            "hile", "algoritma", "sistem", "kasıtlı", "bilerek",
            "rastgele değil", "oyun isterse", "oyun seni yönetiyor",
            "kaybettiriyor", "kurmaca", "adaletsiz", "haksızlık",
            "sahtekarlık", "izin vermiyor", "oynatmıyor",
            "kafana göre", "oyun kurucu oynuyor", "geçme ihtimali yok",
            "kaybeden ben oluyorum", "puanlarım gelmiyor",
            "oyun bizimle oynuyor"
        ],
        "regex": [
            r"(hile|algoritma|sahtekarlık|haksızlık)",
            r"oyun.*(kaybettiriyor|yönetiyor|izin vermiyor|oynatmıyor)",
            r"kafana göre",
            r"rastgele değil",
            r"bilerek.*(kaybettiriyor|vermiyor)"
        ],
        "fuzzy": [
            "hile", "algoritma", "adaletsiz", "haksızlık", "sahtekarlık"
        ]
    },

    "destek_iletisim": {
        "keywords": [
            "destek", "yardım", "yardımcı olur musunuz",
            "iletişime geçemiyorum", "cevap vermiyor",
            "geri dönüş", "sorun bildir", "dikkate alınırsa",
            "çözümü nedir", "düzeltebilir miyiz",
            "müşteri temsilcisi", "ulaşamıyorum",
            "ilgilenmiyor", "açıklama yapın"
        ],
        "regex": [
            r"(destek|yardım|müşteri temsilcisi)",
            r"cevap.*vermiyor",
            r"geri dönüş.*(yok|yapılmadı|vermiyor)",
            r"iletişime.*geçemiyorum",
            r"çözümü.*nedir"
        ],
        "fuzzy": [
            "destek", "yardım", "iletişim", "ulaşamıyorum"
        ]
    },

    "sohbet_takim_arkadas_topluluk": {
        "keywords": [
            "sohbet", "mesaj", "ban", "erişim engeli", "spam engeli",
            "takım", "grup", "lider", "arkadaş",
            "arkadaşlarımı göremiyorum", "arkadaş listem",
            "puanlarını göremiyoruz", "istek gönderemiyorum",
            "konuşamıyorum", "küfür", "hakaret", "oyuncu davet",
            "chat", "kulüp"
        ],
        "regex": [
            r"(sohbet|chat|mesaj|takım|grup|kulüp)",
            r"arkadaş.*(göremiyorum|listem|ekleyemiyorum)",
            r"(ban|erişim engeli|spam engeli)",
            r"(küfür|hakaret)"
        ],
        "fuzzy": [
            "sohbet", "takım", "arkadaş", "chat", "kulüp"
        ]
    },

    "hesap_kayit_ilerleme": {
        "keywords": [
            "hesap", "hesabım", "facebook", "google play", "kayıt",
            "baştan başladı", "sıfırdan", "ilerleme", "kaldığım yerden",
            "telefonuma aktardım", "telefon değişikliği", "format",
            "oyunu silmek istiyorum", "telefon değişti",
            "yeniden başlattı", "levelimi geri alamadım",
            "oyunum silindi", "profil", "avatar", "isim değiştirme",
            "1 seviyeye düştüm", "seviye 1", "geri attı",
            "geriye dönüyor", "sıfırlanma"
        ],
        "regex": [
            r"hesab.*(silindi|gitti|geri alamadım|sıfırlandı)",
            r"(baştan|sıfırdan).*başladı",
            r"level.*geri alamadım",
            r"telefon.*değişti",
            r"(facebook|google play).*bağlan",
            r"ilerleme.*(gitti|silindi|kayboldu)"
        ],
        "fuzzy": [
            "hesap", "kayıt", "ilerleme", "profil", "avatar", "sıfırlandı"
        ]
    },

    "internet_cevrimdisi": {
        "keywords": [
            "internet", "internetsiz", "çevrimdışı", "çevrim dışı",
            "internet yokken", "internet kapalıyken", "internet çekse",
            "internet bağlantısız", "internet olmadan oynanmıyor",
            "internetli", "internetsiz oynanmıyor",
            "internetsiz oynayamıyoruz", "wifi", "online"
        ],
        "regex": [
            r"internet.*(yok|olmadan|kapalı|çekmiyor|istemesin)",
            r"internetsiz.*(oynanmıyor|oynayamıyorum)",
            r"çevrim\s*dışı",
            r"wifi"
        ],
        "fuzzy": [
            "internet", "internetsiz", "çevrimdışı", "wifi", "online"
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
        "fuzzy": [
            "gizlilik", "sözleşme", "izin", "güvenlik"
        ]
    },

    "dil_lokalizasyon": {
        "keywords": [
            "türkçe", "turkce", "ingilizce", "dil", "dil desteği",
            "türkçe değil", "ingilizceye geçiyor",
            "yarı ingilizce", "çeviri", "sorular ingilizce",
            "türkçe olmuyor"
        ],
        "regex": [
            r"türkçe.*(değil|olmuyor|yok)",
            r"ingilizce.*(geçiyor|sorular|oluyor)",
            r"dil.*(desteği|sorunu|yok)",
            r"çeviri"
        ],
        "fuzzy": [
            "türkçe", "turkce", "ingilizce", "çeviri"
        ]
    },

    "uygunsuz_icerik_yas": {
        "keywords": [
            "çocuklar için uygun değil", "küçük çocuklar",
            "yaş sınırı", "uygunsuz", "evlilik", "cinsel",
            "sapık", "kötü örnek", "çocuklara kötü",
            "şiddet", "aldatma"
        ],
        "regex": [
            r"çocuk.*(uygun değil|kötü)",
            r"(yaş sınırı|uygunsuz|cinsel|şiddet|aldatma)",
            r"kötü örnek"
        ],
        "fuzzy": [
            "uygunsuz", "çocuk", "şiddet", "cinsel"
        ]
    },

    "egitici_bilissel_fayda": {
        "keywords": [
            "beyin", "zeka", "zihin", "zihni", "eğitici",
            "öğretici", "hafıza", "kelime haznesi",
            "kelime öğren", "bilgi", "düşünme", "karar verme",
            "iq", "beyin geliştirme", "akıl", "mantık", "bulmaca"
        ],
        "regex": [
            r"(beyin|zeka|zihin|hafıza).*geliştir",
            r"(eğitici|öğretici|bilgi|mantık|bulmaca)",
            r"kelime.*(öğren|haznesi)"
        ],
        "fuzzy": [
            "eğitici", "öğretici", "zeka", "hafıza", "bulmaca"
        ]
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
            "efsane", "müq", "mük", "nice", "good",
            "perfect", "excellent", "iyi oyun", "güzel",
            "iyi", "teşekkürler", "ellerinize sağlık",
            "severek oynuyorum", "favori oyunum", "şahane"
        ],
        "regex": [
            r"(çok|aşırı)?.*(güzel|iyi|harika|mükemmel|süper)",
            r"tavsiye.*ederim",
            r"(beğendim|bayıldım|efsane|şahane)",
            r"severek.*oynuyorum",
            r"ellerinize sağlık"
        ],
        "fuzzy": [
            "güzel", "guzel", "gzl", "iyi", "harika",
            "mükemmel", "mukemmel", "süper", "super", "efsane"
        ]
    },

    "genel_negatif_deneyim": {
        "keywords": [
            "berbat", "rezalet", "çok kötü", "kötü", "saçma",
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
            r"(çok|aşırı)?.*(kötü|berbat|rezalet|saçma)",
            r"zaman.*kaybı",
            r"(oynamayın|indirmeyin|sildim|sileceğim)",
            r"tavsiye.*etmiyorum",
            r"(çöp|gereksiz|boş oyun|bomboş)"
        ],
        "fuzzy": [
            "kötü", "kotu", "berbat", "rezalet", "saçma",
            "çöp", "cop", "gereksiz"
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
        "fuzzy": [
            "düzeltin", "eklenmeli", "olmalı", "geliştirilebilir"
        ]
    },

    "spam_anlamsiz": {
        "keywords": [
            "dudndjd", "hzhhjd", "ndkdj", "full film indir",
            "ak partinin oy oranı", "staff bu arada", "usta yavuz",
            "messi", "bayram", "hüseyin", "anne kakam",
            "sıla ezgi", "ı ı ı", "ok borveg", "old", "ladır"
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