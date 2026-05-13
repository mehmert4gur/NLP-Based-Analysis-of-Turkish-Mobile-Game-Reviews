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
* BERTürk fine-tuning with **class-weighted loss** and **dynamic threshold optimization**
* Streamlit-based interactive analysis UI

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
✅ Train BERTürk multi-label classifier with **CustomTrainer (weighted BCE loss)**
✅ Optimize per-class decision thresholds automatically on validation set
✅ Generate hybrid inference with explainability
✅ Interactive Streamlit UI with **single review analysis** and **dataset dashboard**

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
BERTürk Fine-Tuning (CustomTrainer + Class Weights + Dynamic Thresholds)
        ↓
Evaluation & Error Analysis
        ↓
Hybrid Rule + Transformer Inference
        ↓
Streamlit Interactive UI (Single Analysis + Dataset Dashboard)
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
accelerate \
safetensors \
streamlit
```

---

# 📂 Project Structure

```text
src/
│
├── get_reviews.py                          # Google Play review scraper
├── preprocess_reviews.py                   # Text normalization & cleaning
├── analyze_categories.py                   # Rule-based category detection
├── aspect_sentiment.py                     # Local aspect sentiment extraction
├── category_rules.py                       # Category rule definitions
├── sentiment_rules.py                      # Sentiment rule definitions
│
├── prepare_training_data.py                # Weakly supervised dataset generation
├── analyze_label_distribution.py           # Label distribution analysis
│
├── train_multilabel_berturk.py             # Pilot training (debugging)
├── train_multilabel_berturk_full.py        # Full training (CustomTrainer + dynamic thresholds)
├── predict_multilabel_berturk.py           # Standalone prediction
│
├── evaluate_multilabel_berturk.py          # Model evaluation
├── error_analysis_multilabel_berturk.py    # FP/FN error analysis
├── compare_rule_vs_berturk.py              # Rule vs BERT comparison
│
├── hybrid_inference.py                     # Hybrid inference engine
├── app.py                                  # Streamlit UI (single analysis + dataset dashboard)
├── visualize_results.py                    # Chart/figure generation
│
└── local_games.py                          # Local game definitions
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

## Full Training (with Performance Optimizations)

Full BERTürk fine-tuning with **class imbalance handling** and **dynamic threshold optimization**.

```bash
python src/train_multilabel_berturk_full.py
```

### Key Features

**CustomTrainer with Class Weights:**

The training script uses a custom `Trainer` subclass that overrides `compute_loss` to apply `BCEWithLogitsLoss` with per-class `pos_weight`. This gives the model a higher penalty for misclassifying minority classes, directly addressing the class imbalance problem.

* `pos_weight` is calculated from training set label frequencies
* Extreme weights are clamped at `max=10.0` to prevent instability

**Dynamic Threshold Optimization:**

Instead of using a single global threshold (e.g. 0.35) for all classes, the system searches the optimal threshold for each class individually on the validation set:

* Search range: 0.10 – 0.90 (step 0.05)
* Objective: maximize per-class F1 score
* Result: class-specific thresholds saved to `class_thresholds.json`
* Test evaluation uses **only** validation-tuned thresholds (no data leakage)

**Training Stabilization:**

* `warmup_ratio=0.1` is used to prevent aggressive early weight updates
* Best model is selected based on `macro_f1` on the validation set

### Per-Class Logging

After each evaluation epoch, a detailed per-class report is printed:

```text
Kategori                       | Thresh | F1     | Prec   | Rec    | Support
-------------------------------+--------+--------+--------+--------+--------
reklam                         | 0.40   | 0.9012 | 0.8834 | 0.9198 | 1200
gizlilik_guvenlik_izin       * | 0.20   | 0.4500 | 0.5000 | 0.4091 | 16
```

Categories with support < 50 are marked with `*` for quick identification.

### Outputs

```text
outputs/models/berturk_multilabel_absa_full/
├── best_model/             # Saved model weights & tokenizer
├── class_thresholds.json   # Per-class optimized thresholds
├── val_metrics.json        # Validation set metrics
└── test_metrics.json       # Test set metrics
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

# 🖥️ Interactive Streamlit UI

The project includes a Streamlit-based web interface with **two modes**:

```bash
streamlit run src/app.py
```

## Mode 1: Single Review Analysis (Yapay Zeka)

Analyze a single Turkish game review in real-time using the Hybrid BERTürk + Rule-Based engine.

Features:

* text input or example review selection
* optional star rating input for contradiction detection
* final hybrid categories with confidence levels
* aspect sentiment and local aspect sentiment badges
* main product insight with severity, team assignment and suggested action
* BERTürk top predictions with probability bars
* hybrid decision flow visualization
* explainability panel with rule evidence
* sentiment detail breakdown
* rule vs BERTürk comparison
* uncertain prediction alerts
* full JSON debug output

## Mode 2: Dataset Dashboard (Oyun Veri Seti İnceleme)

Explore and filter the full analyzed dataset interactively.

Features:

* key metrics: total reviews, game count, analyzable reviews
* game-based filtering (selectbox)
* category complaint distribution bar chart (top 15)
* interactive searchable and sortable data table with columns:
  * game name, rating, review text, categories, sentiment, date

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

This is addressed by the **CustomTrainer with pos_weight** and **dynamic threshold optimization** in the training pipeline.

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
✅ Full BERTürk training with CustomTrainer
✅ Hybrid inference system
✅ Streamlit UI (single analysis + dataset dashboard)

---

# 📌 Known Challenges

## Dataset Imbalance

Some categories are extremely rare.

Example:

```text
olumlu_deneyim → 10533
gizlilik_guvenlik_izin → 16
```

Implemented solutions:

* ✅ weighted loss (BCEWithLogitsLoss with pos_weight)
* ✅ per-class threshold tuning
* ✅ warmup ratio for training stabilization

Potential future improvements:

* oversampling / data augmentation
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

## Phase 1 — ✅ Full BERTürk ABSA Training (Completed)

Train full multi-label category classifier with class-weighted loss and dynamic thresholds.

---

## Phase 2 — Full Evaluation & Error Analysis

Analyze:

* rare label failures
* false positives
* semantic confusion
* dominant label bias

---

## Phase 3 — ✅ Hybrid Rule + BERT System (Completed)

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
