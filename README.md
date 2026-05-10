<div align="center">
  <h1>Turkish Mobile Game Reviews ABSA Pipeline</h1>
  
  <p>
    <a href="https://github.com/yourusername/NLP-Based-Analysis-of-Turkish-Mobile-Game-Reviews/actions"><img src="https://img.shields.io/github/actions/workflow/status/yourusername/NLP-Based-Analysis-of-Turkish-Mobile-Game-Reviews/test.yml?branch=main" alt="Build Status"></a>
    <a href="https://www.python.org/downloads/release/python-3.9.0/"><img src="https://img.shields.io/badge/python-3.9%2B-blue.svg" alt="Python Version"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  </p>
</div>

---

## 📖 Project Overview

An end-to-end Natural Language Processing pipeline for Aspect-Based Sentiment Analysis (ABSA) and topic modeling on Turkish mobile game reviews. Designed for high precision on morphologically rich, unstructured user feedback. 

This project automatically scrapes reviews from the Google Play Store for defined local games, normalizes agglutinative Turkish text structures, classifies them into domain-specific categories (like *monetization*, *performance*, *UI/UX*), and determines sentiment polarity.

---

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/NLP-Based-Analysis-of-Turkish-Mobile-Game-Reviews.git
   cd NLP-Based-Analysis-of-Turkish-Mobile-Game-Reviews
   ```

2. **Initialize a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   To run this pipeline, you need specific packages for data manipulation, fuzzy string matching, and web scraping. Execute the following command:
   ```bash
   python -m pip install google-play-scraper pandas tqdm openpyxl rapidfuzz
   ```

---

## 🧪 Testing & Development

The project includes a comprehensive unit test suite to ensure the NLP rules and preprocessing steps remain stable as you add new features or categories.

**1. Install all dependencies (including testing tools):**
```bash
python -m pip install -r requirements.txt
```

**2. Run the entire test suite:**
```bash
python -m pytest
```

**3. Run specific test files:**
```bash
python -m pytest tests/test_preprocess_reviews.py
python -m pytest tests/test_analyze_categories.py
```

---

## 🚀 How to Run

The pipeline consists of three main sequential scripts. You must run them in the order listed below to successfully fetch, process, and analyze the review data.

---

## 🔄 Pipeline Steps

### 1. Data Ingestion
Scrapes the newest and most relevant reviews for the mobile games defined in `src/local_games.py` from the Google Play Store.

```bash
python src/get_reviews.py
```
*Note: This script will take some time depending on your internet connection and the number of games/reviews configured. It fetches up to 1000 newest and 1000 most relevant reviews per game by default.*

### 2. Preprocessing & Normalization
Cleans the raw text data. It removes URLs, emojis, and special characters. Crucially, it normalizes common Turkish text variations, typos, and repeated characters specifically found in mobile game reviews.

```bash
python src/preprocess_reviews.py
```

### 3. Aspect-Based Sentiment Inference
Runs the preprocessed text through a deterministic, high-precision lexio-syntactic rule engine and fuzzy matchers (`category_rules.py` and `sentiment_rules.py`). It assigns categories, extracts local aspect sentiments, and checks for contradictions (e.g., giving 5 stars but writing a highly negative review).

```bash
python src/analyze_categories.py
```

---

## 📂 Output Files

As you execute the pipeline, the following structured artifacts are generated in the `data/` directory:

### Raw Data (`data/raw/`)
- `yerel_oyun_yorumlari.xlsx` & `.csv`: Raw scraped datasets with original text, metadata, and timestamps.

### Processed Data (`data/processed/`)
- `temiz_yorumlar.xlsx`: Cleaned and normalized text with flags indicating if the review is analyzable (is_probably_turkish, is_meaningful_short, etc.).
- `kategori_analizi.xlsx`: The main output file containing the assigned categories and general sentiment scores for all analyzable reviews.
- `kategorisiz_yorumlar.xlsx`: Reviews that the pipeline couldn't match to any known category rules.
- `coklu_kategorili_yorumlar.xlsx`: Complex reviews containing 4 or more distinct topic categories.
- `kategori_ornekleri.xlsx`: A subset (up to 30) of reviews per category for quick manual validation.
- `kategori_eslesme_detaylari.xlsx`: Transparency logs showing exactly *why* a category was assigned (keyword match, regex match, near match, or fuzzy match).
- `sentiment_analizi_detaylari.xlsx`: Detailed scoring breakdown of positive, negative, and neutral tokens.
- `local_aspect_sentiment_details.xlsx`: Granular aspect-level polarity (e.g., negative towards "reklam", positive towards "grafik").
- `rating_text_contradictions.xlsx`: Edge-case logs where the star rating heavily contradicts the calculated text sentiment.

---

## 📊 Visualization

After running the full pipeline, you can generate summary charts from the analysis output.

**Install the visualization dependency:**
```bash
python -m pip install matplotlib
```
*(Or install all dependencies at once with `python -m pip install -r requirements.txt`)*

**Run the visualization script:**
```bash
python src/visualize_results.py
```

All figures are saved to **`outputs/figures/`**:

| File | Description |
| :--- | :--- |
| `category_distribution.png` | Bar chart showing how many reviews were tagged with each category (e.g., `reklam`, `performans_donma_kasma`). |
| `rating_distribution.png` | Bar chart of the 1–5 star rating distribution across all scraped reviews. |
| `monthly_review_count.png` | Line chart of review volume per calendar month, useful for spotting spikes after updates or events. |
| `category_count_distribution.png` | Bar chart showing how many reviews have 0, 1, 2, 3, or 4+ categories assigned — a proxy for review complexity. |

---

## 📌 Notes

- **Package Installation Note**: During the test run, if `pip install ...` results in a `"pip is not recognized"` error on Windows, always use `python -m pip install ...` to correctly map the package manager to your current Python environment.
- **Execution Success**: The pipeline was successfully run and validated end-to-end. No logical errors or crashes were encountered across ingestion, preprocessing, or categorization.
- **Customizing Games**: To change which games are scraped, update the `LOCAL_GAMES` list inside `src/local_games.py` with the correct `app_id` (Google Play Package Name).
- **Customizing Rules**: To add new categories or sentiment words, modify the dictionaries in `src/category_rules.py` and `src/sentiment_rules.py`.
