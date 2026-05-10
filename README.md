# Turkish Mobile Game Reviews ABSA Pipeline

<div align="center">

# Turkish Mobile Game Reviews ABSA Pipeline

### Hybrid Rule-Based + BERTürk NLP System for Turkish Mobile Game Review Analysis

<p>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg">
  <img src="https://img.shields.io/badge/NLP-ABSA-green.svg">
  <img src="https://img.shields.io/badge/Transformers-BERTurk-orange.svg">
  <img src="https://img.shields.io/badge/Status-Research%20%26%20Development-yellow.svg">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey.svg">
</p>

</div>

---

# 📖 Project Overview

This project is an end-to-end NLP pipeline for **Aspect-Based Sentiment Analysis (ABSA)** on Turkish mobile game reviews collected from the Google Play Store.

The system combines:

* deterministic rule-based NLP
* fuzzy matching
* regex and proximity rules
* local aspect sentiment extraction
* weakly supervised dataset generation
* BERTürk fine-tuning infrastructure

to create a scalable and explainable Turkish review analysis system.

The long-term goal is to build a:

```text
Hybrid Rule-Based + Transformer-Based ABSA System
```

capable of understanding:

* what users are talking about
* which game aspects are criticized or praised
* sentiment polarity
* aspect-level sentiment
* contradictions between star ratings and review text
* semantic category relations

---

# 🎯 Current Capabilities

The current system can:

✅ Scrape Turkish mobile game reviews from Google Play
✅ Normalize noisy Turkish user text
✅ Detect categories/aspects using rule-based NLP
✅ Extract local aspect sentiment
✅ Detect rating-text contradictions
✅ Generate explainable analysis outputs
✅ Build weakly supervised training datasets
✅ Run pilot BERTürk multi-label training
✅ Generate hybrid inference infrastructure

---

# 🧠 Supported Categories

The rule engine currently supports categories such as:

```text
reklam
performans_donma_kasma
crash_hata_bug
yukleme_acilis_sorunu
zorluk_level_design
odeme_satin_alma_ekonomi
odul_bonus_ipucu
kart_koleksiyon
hile_algoritma_adalet
yaniltici_reklam_tanitim
olumlu_deneyim
genel_negatif_deneyim
```

and many more.

The system currently contains approximately:

```text
26 multi-label aspect categories
```

---

# 🏗️ System Architecture

```text
Google Play Reviews
        ↓
Data Collection
        ↓
Preprocessing & Normalization
        ↓
Rule-Based Category Detection
        ↓
Sentiment Analysis
        ↓
Local Aspect Sentiment Extraction
        ↓
Weakly Supervised Dataset Generation
        ↓
BERTürk Fine-Tuning
        ↓
Evaluation & Error Analysis
        ↓
Hybrid Rule + Transformer Inference
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/yourusername/NLP-Based-Analysis-of-Turkish-Mobile-Game-Reviews.git
cd NLP-Based-Analysis-of-Turkish-Mobile-Game-Reviews
```

---

## 2. Create virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

Or manually:

```bash
python -m pip install \
google-play-scraper \
pandas \
numpy \
openpyxl \
rapidfuzz \
tqdm \
matplotlib \
scikit-learn \
transformers \
datasets \
torch \
accelerate
```

---

# 📂 Project Structure

```text
src/
│
├── get_reviews.py
├── preprocess_reviews.py
├── analyze_categories.py
├── aspect_sentiment.py
├── category_rules.py
├── sentiment_rules.py
│
├── prepare_training_data.py
├── analyze_label_distribution.py
│
├── train_multilabel_berturk.py
├── train_multilabel_berturk_full.py
├── predict_multilabel_berturk.py
│
├── evaluate_multilabel_berturk.py
├── error_analysis_multilabel_berturk.py
├── compare_rule_vs_berturk.py
│
├── hybrid_inference.py
├── visualize_results.py
│
└── local_games.py
```

---

# 🚀 Pipeline Steps

---

# 1. Data Collection

Scrapes reviews from Google Play Store.

```bash
python src/get_reviews.py
```

Outputs:

```text
data/raw/yerel_oyun_yorumlari.xlsx
data/raw/yerel_oyun_yorumlari.csv
```

---

# 2. Preprocessing & Normalization

Cleans and normalizes Turkish review text.

Features:

* typo normalization
* repeated character reduction
* Turkish text normalization
* URL cleanup
* emoji cleanup
* analyzable review filtering

```bash
python src/preprocess_reviews.py
```

Output:

```text
data/processed/temiz_yorumlar.xlsx
```

---

# 3. Rule-Based ABSA Analysis

Runs deterministic NLP category and sentiment analysis.

Features:

* keyword matching
* fuzzy matching
* regex matching
* near/proximity matching
* category assignment
* general sentiment
* local aspect sentiment
* contradiction detection

```bash
python src/analyze_categories.py
```

Outputs:

```text
kategori_analizi.xlsx
kategorisiz_yorumlar.xlsx
coklu_kategorili_yorumlar.xlsx
kategori_eslesme_detaylari.xlsx
sentiment_analizi_detaylari.xlsx
local_aspect_sentiment_details.xlsx
rating_text_contradictions.xlsx
```

---

# 4. Visualization

Generates summary figures and statistics.

```bash
python src/visualize_results.py
```

Outputs:

```text
outputs/figures/
```

Includes:

* category distribution
* rating distribution
* review count trends
* category complexity distribution

---

# 🧪 Weakly Supervised Dataset Generation

The rule-based outputs are converted into training datasets for BERTürk fine-tuning.

```bash
python src/prepare_training_data.py
```

Generated datasets:

```text
data/training/

absa_multilabel_train.csv
absa_multilabel_val.csv
absa_multilabel_test.csv

sentiment_train.csv
sentiment_val.csv
sentiment_test.csv

label_map.json
sentiment_label_map.json
```

---

# 🤖 BERTürk Multi-Label Training

## Pilot Training

Small-scale debugging and infrastructure validation.

```bash
python src/train_multilabel_berturk.py
```

Purpose:

* verify training pipeline
* validate tokenizer/model setup
* test multi-label classification
* validate metrics and saving

---

## Full Training

Full BERTürk fine-tuning on the generated dataset.

```bash
python src/train_multilabel_berturk_full.py
```

Outputs:

```text
outputs/models/berturk_multilabel_absa_full/
```

---

# 📊 Model Evaluation

Evaluates the trained model on the test dataset.

```bash
python src/evaluate_multilabel_berturk.py
```

Metrics:

* micro F1
* macro F1
* precision
* recall
* per-label classification report

Outputs:

```text
overall_metrics.json
per_label_classification_report.csv
test_predictions.csv
```

---

# 🔍 Error Analysis

Analyzes false positives and false negatives.

```bash
python src/error_analysis_multilabel_berturk.py
```

Outputs:

```text
false_positives.xlsx
false_negatives.xlsx
error_summary.csv
```

---

# ⚖️ Rule-Based vs BERTürk Comparison

Compares rule-based outputs with transformer predictions.

```bash
python src/compare_rule_vs_berturk.py
```

Outputs:

```text
rule_vs_berturk_summary.csv
rule_vs_berturk_disagreements.xlsx
berturk_only_predictions.xlsx
rule_only_predictions.xlsx
```

---

# 🧩 Hybrid Inference System

Combines:

* rule-based categories
* BERTürk predictions
* confidence thresholds

to generate final decisions.

```bash
python src/hybrid_inference.py
```

Current hybrid logic:

```text
Rule-based → high precision
BERTürk → semantic generalization
Hybrid → final explainable inference
```

---

# 📈 Current Dataset Statistics

Current processed dataset:

```text
~18K analyzed Turkish mobile game reviews
~26 multi-label categories
```

Observed issue:

```text
Strong label imbalance
```

Example:

```text
olumlu_deneyim → 10K+
gizlilik_guvenlik_izin → 16
```

This is currently one of the biggest research challenges in the project.

---

# 🧪 Current Project Status

## Successfully Tested

✅ Review scraping
✅ Preprocessing pipeline
✅ Rule-based category detection
✅ Sentiment analysis
✅ Aspect sentiment extraction
✅ Dataset generation
✅ Pilot BERTürk training
✅ Pilot prediction pipeline

---

## Written but Not Fully Tested Yet

⚠️ Full BERTürk training
⚠️ Full evaluation pipeline
⚠️ Error analysis pipeline
⚠️ Rule vs BERT comparison
⚠️ Hybrid inference system

These components are prepared but require stronger hardware and full-scale training.

---

# 📌 Known Challenges

## Dataset Imbalance

Some categories are extremely rare.

Example:

```text
olumlu_deneyim → 10533
gizlilik_guvenlik_izin → 16
```

Potential solutions:

* weighted loss
* oversampling
* threshold tuning
* manual annotation
* active learning

---

## Weak Label Noise

Current BERT training labels are generated from the rule engine.

Therefore:

```text
Dataset = weakly supervised
```

not fully gold-labeled.

---

## CPU Training Speed

Transformer training on CPU is extremely slow.

Recommended:

* CUDA GPU
* Google Colab
* Kaggle
* dedicated ML workstation

---

# 🔮 Future Roadmap

## Phase 1 — Full BERTürk ABSA Training

Train full multi-label category classifier.

---

## Phase 2 — Full Evaluation & Error Analysis

Analyze:

* rare label failures
* false positives
* semantic confusion
* dominant label bias

---

## Phase 3 — Hybrid Rule + BERT System

Combine deterministic precision with semantic learning.

---

## Phase 4 — BERTürk Sentiment Model

Train:

```text
review → sentiment
```

classifier.

---

## Phase 5 — Aspect-Level Sentiment Model

True ABSA target:

```text
(review + aspect) → sentiment
```

Example:

```text
"oyun güzel ama reklam çok fazla"
+
"reklam"
→ negative
```

---

# 📊 Research Goals

This project aims to become:

```text
A scalable, explainable, Turkish Aspect-Based Sentiment Analysis framework
for mobile game review mining.
```

Potential applications:

* mobile game analytics
* player feedback intelligence
* update impact analysis
* monetization analysis
* automated QA feedback mining
* Turkish NLP research

---

# 📌 Notes

## Windows pip Issue

If you encounter:

```text
pip is not recognized
```

always use:

```bash
python -m pip install ...
```

instead.

---

## GPU Note

If full training crashes with:

```text
fp16 error
```

set:

```python
fp16=False
```

inside training scripts.

---

# 📜 License

MIT License

---

# 👥 Contributors

This project is actively evolving as a hybrid NLP + Transformer research pipeline for Turkish mobile game review analysis.

Contributions, experiments, and research ideas are welcome.
