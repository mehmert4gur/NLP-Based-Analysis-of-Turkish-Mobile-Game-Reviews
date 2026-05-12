import streamlit as st

from hybrid_inference import load_model, analyze_review_for_ui


st.set_page_config(
    page_title="BERTürk Hybrid ABSA Demo",
    page_icon="🎮",
    layout="wide",
)


CUSTOM_CSS = """
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    padding: 1.4rem 1.6rem;
    border-radius: 18px;
    background: linear-gradient(135deg, #171717 0%, #2d2d2d 100%);
    color: white;
    margin-bottom: 1.5rem;
}

.hero h1 {
    margin-bottom: 0.3rem;
}

.hero p {
    opacity: 0.85;
    font-size: 1.05rem;
}

.metric-card {
    padding: 1rem;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    background: #ffffff;
}

.small-muted {
    color: #6b7280;
    font-size: 0.92rem;
}

.badge {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-right: 0.25rem;
}

.badge-high {
    background: #dcfce7;
    color: #166534;
}

.badge-medium {
    background: #fef9c3;
    color: #854d0e;
}

.badge-low {
    background: #ffedd5;
    color: #9a3412;
}

.badge-neutral {
    background: #f3f4f6;
    color: #374151;
}

.badge-negative {
    background: #fee2e2;
    color: #991b1b;
}

.badge-positive {
    background: #dcfce7;
    color: #166534;
}

.badge-mixed {
    background: #ffedd5;
    color: #9a3412;
}

.badge-unknown {
    background: #e5e7eb;
    color: #374151;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_resource(show_spinner="Model yükleniyor...")
def cached_model():
    return load_model()


def badge(label, kind="neutral"):
    return f"<span class='badge badge-{kind}'>{label}</span>"


def confidence_kind(level):
    if level == "high":
        return "high"
    if level == "medium":
        return "medium"
    if level == "low":
        return "low"
    return "neutral"


def confidence_text(level):
    if level == "high":
        return "Yüksek güven"
    if level == "medium":
        return "Orta güven"
    if level == "low":
        return "Düşük güven"
    return "Rule / düşük BERT olasılığı"


def sentiment_kind(sentiment):
    if sentiment == "positive":
        return "positive"
    if sentiment == "negative":
        return "negative"
    if sentiment == "mixed":
        return "mixed"
    if sentiment == "neutral":
        return "neutral"
    return "unknown"


def severity_kind(severity):
    if severity == "high":
        return "negative"
    if severity == "medium":
        return "mixed"
    return "positive"


def source_label(source):
    labels = {
        "bert_high_confidence": "BERTürk yüksek güven",
        "rule_and_bert_agree": "Rule + BERTürk uyumlu",
        "rule_based": "Rule-based",
    }
    return labels.get(source, source)


def render_probability_bar(label, probability, caption=None):
    probability = float(probability)
    st.progress(
        min(max(probability, 0), 1),
        text=f"{label} — {probability:.2%}" if caption is None else caption,
    )


def render_category_card(item, result):
    category = item["category"]
    aspect_sentiment = result["sentiment"]["aspect_sentiments"].get(category, "unknown")
    local_sentiment = result["sentiment"]["local_aspect_sentiments"].get(category, "unknown")

    with st.container(border=True):
        st.markdown(f"### {item['display_name']}")

        st.markdown(
            badge(confidence_text(item["confidence_level"]), confidence_kind(item["confidence_level"]))
            + badge(f"Aspect: {aspect_sentiment}", sentiment_kind(aspect_sentiment))
            + badge(f"Local: {local_sentiment}", sentiment_kind(local_sentiment)),
            unsafe_allow_html=True,
        )

        st.write("")
        render_probability_bar(
            "BERTürk olasılığı",
            item["probability"],
            caption=f"BERTürk olasılığı — {float(item['probability']):.2%}",
        )

        st.caption(f"Kategori kodu: `{category}`")


def render_main_issue(result):
    main_issue = result["product_insight"]["main_issue"]

    if not main_issue:
        st.info("Ana ürün içgörüsü bulunamadı.")
        return

    st.markdown("### Ana Ürün İçgörüsü")

    with st.container(border=True):
        st.markdown(f"## {main_issue['display_name']}")

        st.markdown(
            badge(f"Şiddet: {main_issue['severity']}", severity_kind(main_issue["severity"]))
            + badge(f"Sentiment: {main_issue['sentiment']}", sentiment_kind(main_issue["sentiment"])),
            unsafe_allow_html=True,
        )

        st.write("")
        st.write(f"**İlgili ekip:** {main_issue['team']}")
        st.write(f"**Önerilen aksiyon:** {main_issue['suggested_action']}")


def render_warning_box(warnings):
    if not warnings:
        st.success("Özel uyarı yok.")
        return

    for warning in warnings:
        if warning["level"] == "high":
            st.error(warning["message"])
        else:
            st.warning(warning["message"])


def render_decision_flow(result):
    st.subheader("Hybrid Karar Akışı")

    decision_details = result["categories"]["decision_details"]

    if not decision_details:
        st.info("Karar detayı bulunamadı.")
        return

    for detail in decision_details:
        with st.container(border=True):
            col1, col2, col3 = st.columns([1.3, 1, 1])

            with col1:
                st.write(f"**{detail['display_name']}**")
                st.caption(f"`{detail['category']}`")

            with col2:
                st.write("Kaynak")
                st.markdown(badge(source_label(detail["source"]), "neutral"), unsafe_allow_html=True)

            with col3:
                st.write("Olasılık")
                st.write(f"**{float(detail['probability']):.2%}**")


def render_explanations(result):
    explanations = result["explanations"]

    if not explanations:
        st.info("Açıklama bulunamadı.")
        return

    for _, explanation in explanations.items():
        with st.container(border=True):
            st.markdown(f"### {explanation['display_name']}")

            st.markdown(
                badge(source_label(explanation["source"]), "neutral")
                + badge(confidence_text(explanation["confidence_level"]), confidence_kind(explanation["confidence_level"])),
                unsafe_allow_html=True,
            )

            st.write("")
            st.write(explanation["explanation"])
            st.write(f"**BERTürk olasılığı:** {float(explanation['probability']):.2%}")

            evidence = explanation.get("rule_evidence", [])

            if evidence:
                st.write("**Rule evidence:**")
                for ev in evidence:
                    st.code(f"{ev.get('match_type', '')}: {ev.get('evidence', '')}")


def render_sentiment_details(result):
    sentiment = result["sentiment"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Pozitif skor", sentiment["positive_score"])

    with col2:
        st.metric("Negatif skor", sentiment["negative_score"])

    with col3:
        st.metric("Final sentiment skoru", sentiment["sentiment_score"])

    st.write("### Sentiment Evidence")

    evidence = sentiment["sentiment_evidence"]

    if evidence:
        for ev in evidence:
            st.code(ev)
    else:
        st.info("Sentiment evidence bulunamadı.")

    st.write("### Aspect Sentiment Dağılımı")
    st.json(result["statistics"]["aspect_sentiment_summary"])

    st.write("### Local Aspect Sentiment Dağılımı")
    st.json(result["statistics"]["local_aspect_sentiment_summary"])


def render_model_comparison(result):
    agreement = result["statistics"]["agreement"]

    st.subheader("Rule-Based vs BERTürk Karşılaştırması")

    st.metric("Uyum skoru", agreement["score"])
    st.write(agreement["interpretation"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Ortak kategoriler**")
        if agreement["common_categories"]:
            for item in agreement["common_categories"]:
                st.success(item)
        else:
            st.caption("Yok")

    with col2:
        st.write("**Sadece rule-based**")
        if agreement["rule_only_categories"]:
            for item in agreement["rule_only_categories"]:
                st.warning(item)
        else:
            st.caption("Yok")

    with col3:
        st.write("**Sadece BERTürk**")
        if agreement["bert_only_categories"]:
            for item in agreement["bert_only_categories"]:
                st.info(item)
        else:
            st.caption("Yok")


def render_bert_predictions(result):
    st.subheader("En Yüksek BERTürk Tahminleri")

    for item in result["categories"]["bert_top_predictions"]:
        render_probability_bar(
            item["display_name"],
            item["probability"],
            caption=(
                f"{item['display_name']} — "
                f"{float(item['probability']):.2%} — "
                f"{confidence_text(item['confidence_level'])}"
            ),
        )


def render_uncertain_predictions(result):
    uncertain = result["categories"]["uncertain_predictions"]

    if not uncertain:
        st.success("Dikkat çekici kararsız tahmin yok.")
        return

    for item in uncertain:
        with st.container(border=True):
            st.write(f"**{item['display_name']}**")
            st.write(f"Olasılık: **{float(item['probability']):.2%}**")
            st.caption(item["reason"])


st.markdown(
    """
    <div class="hero">
        <h1>🎮 Türkçe Mobil Oyun Yorumu Analizi</h1>
        <p>
            Hybrid BERTürk + Rule-Based ABSA sistemiyle yorumlardan kategori,
            sentiment, güven skoru, açıklama ve ürün aksiyonu çıkarımı.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.header("Model Paneli")
    st.write("**Model:** BERTürk Multi-label ABSA")
    st.write("**Yaklaşım:** Hybrid")
    st.write("**Girdi:** Türkçe oyun yorumu")
    st.write("**Çıktı:** Kategori + sentiment + explainability")

    st.divider()

    rating = st.selectbox(
        "Yıldız puanı",
        ["Yok", 1, 2, 3, 4, 5],
        index=0,
        help="Opsiyonel. Girilirse rating-text contradiction kontrolü yapılır.",
    )

    rating_value = None if rating == "Yok" else rating

    st.divider()

    st.write("### Eşik Açıklaması")
    st.caption("0.60+ → yüksek güven")
    st.caption("0.45–0.60 → orta güven")
    st.caption("0.35–0.45 → düşük güven")
    st.caption("0.25–0.35 → kararsız / dikkat çekici")


tokenizer, model, device = cached_model()


example_texts = [
    "oyun güzel ama çok reklam var ve sürekli kasıyor",
    "reklamdaki oyunla alakası yok bambaşka bir şey çıkıyor",
    "oyun açılmıyor sürekli hata veriyor",
    "bölümler çok zor hamle yetmiyor",
    "kart vermiyor hep aynı kart çıkıyor",
    "çok güzel eğlenceli bir oyun herkese tavsiye ederim",
    "5 yıldız verdim yorumum üstte gözüksün ama oyun çok kötü",
]


st.subheader("Yorum Girişi")

selected_example = st.selectbox(
    "Örnek yorum seç",
    ["Kendi yorumumu yazacağım"] + example_texts,
)

default_text = "" if selected_example == "Kendi yorumumu yazacağım" else selected_example

text = st.text_area(
    "Analiz edilecek yorum",
    value=default_text,
    height=150,
    placeholder="Buraya bir oyun yorumu yaz...",
)

col_button, col_clear = st.columns([1, 5])

with col_button:
    analyze_button = st.button("Analiz Et", type="primary", use_container_width=True)

with col_clear:
    st.caption("Metin girildikten sonra model kategori, sentiment ve ürün aksiyonu üretecek.")


if analyze_button:
    if not text.strip():
        st.warning("Lütfen analiz edilecek bir yorum gir.")
        st.stop()

    with st.spinner("Yorum analiz ediliyor..."):
        result = analyze_review_for_ui(
            text=text,
            rating=rating_value,
            tokenizer=tokenizer,
            model=model,
            device=device,
        )

    if not result.get("success"):
        st.error(result.get("error", "Analiz sırasında hata oluştu."))
        st.stop()

    st.divider()

    sentiment = result["sentiment"]["general_sentiment"]

    st.subheader("Özet Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Final kategori", result["statistics"]["final_category_count"])

    with col2:
        st.metric("Rule kategori", result["statistics"]["rule_category_count"])

    with col3:
        st.metric("BERT eşik üstü", result["statistics"]["bert_threshold_category_count"])

    with col4:
        st.metric("Rule-BERT uyumu", result["statistics"]["agreement"]["score"])

    st.markdown(
        badge(f"Genel sentiment: {sentiment}", sentiment_kind(sentiment))
        + badge(f"Sentiment skoru: {result['sentiment']['sentiment_score']}", "neutral"),
        unsafe_allow_html=True,
    )

    st.write("")

    left, right = st.columns([1.4, 1])

    with left:
        st.subheader("Final Hybrid Kategoriler")

        final_categories = result["categories"]["final_categories"]

        if not final_categories:
            st.info("Kategori bulunamadı.")
        else:
            for item in final_categories:
                render_category_card(item, result)

    with right:
        render_main_issue(result)

        st.write("")
        st.subheader("Uyarılar")
        render_warning_box(result["warnings"])

    st.divider()

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "BERTürk Tahminleri",
            "Karar Akışı",
            "Açıklamalar",
            "Sentiment",
            "Rule vs BERTürk",
            "Kararsız Tahminler",
            "Debug JSON",
        ]
    )

    with tab1:
        render_bert_predictions(result)

    with tab2:
        render_decision_flow(result)

    with tab3:
        render_explanations(result)

    with tab4:
        render_sentiment_details(result)

    with tab5:
        render_model_comparison(result)

    with tab6:
        render_uncertain_predictions(result)

    with tab7:
        with st.expander("Ham JSON çıktısını göster", expanded=False):
            st.json(result)