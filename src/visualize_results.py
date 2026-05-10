import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend, safe for scripts
import matplotlib.pyplot as plt
from pathlib import Path
from ast import literal_eval

INPUT_PATH = Path("data/processed/kategori_analizi.xlsx")
OUTPUT_DIR = Path("outputs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    df = pd.read_excel(INPUT_PATH)

    # categories column is stored as a stringified list — parse it back
    if "categories" in df.columns:
        df["categories"] = df["categories"].apply(
            lambda x: literal_eval(x) if isinstance(x, str) else (x if isinstance(x, list) else [])
        )

    if "review_created_at" in df.columns:
        df["review_created_at"] = pd.to_datetime(df["review_created_at"], errors="coerce")

    return df


def plot_category_distribution(df):
    """Bar chart: how many reviews were tagged with each category."""
    exploded = df.explode("categories").dropna(subset=["categories"])
    exploded = exploded[exploded["categories"].str.strip() != ""]
    counts = exploded["categories"].value_counts()

    fig, ax = plt.subplots(figsize=(12, 6))
    counts.plot(kind="bar", ax=ax, color="#4C72B0", edgecolor="white")
    ax.set_title("Category Distribution", fontsize=14, fontweight="bold")
    ax.set_xlabel("Category")
    ax.set_ylabel("Number of Reviews")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "category_distribution.png", dpi=150)
    plt.close(fig)
    print("Saved: outputs/figures/category_distribution.png")


def plot_rating_distribution(df):
    """Bar chart: distribution of star ratings."""
    rating_col = next((c for c in ["rating", "score", "stars"] if c in df.columns), None)

    if rating_col is None:
        print("Skipping rating_distribution: no rating column found.")
        return

    counts = df[rating_col].dropna().astype(int).value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(7, 5))
    counts.plot(kind="bar", ax=ax, color="#55A868", edgecolor="white")
    ax.set_title("Rating Distribution", fontsize=14, fontweight="bold")
    ax.set_xlabel("Star Rating")
    ax.set_ylabel("Number of Reviews")
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "rating_distribution.png", dpi=150)
    plt.close(fig)
    print("Saved: outputs/figures/rating_distribution.png")


def plot_monthly_review_count(df):
    """Line chart: number of reviews per month over time."""
    if "review_created_at" not in df.columns:
        print("Skipping monthly_review_count: no review_created_at column found.")
        return

    monthly = (
        df.dropna(subset=["review_created_at"])
        .set_index("review_created_at")
        .resample("ME")
        .size()
    )

    if monthly.empty:
        print("Skipping monthly_review_count: no valid date data.")
        return

    fig, ax = plt.subplots(figsize=(12, 5))
    monthly.plot(kind="line", ax=ax, marker="o", color="#C44E52", linewidth=2, markersize=4)
    ax.set_title("Monthly Review Count", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Reviews")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "monthly_review_count.png", dpi=150)
    plt.close(fig)
    print("Saved: outputs/figures/monthly_review_count.png")


def plot_category_count_distribution(df):
    """Bar chart: how many reviews have 0, 1, 2, 3, 4+ categories."""
    if "category_count" not in df.columns:
        df["category_count"] = df["categories"].apply(
            lambda x: len(x) if isinstance(x, list) else 0
        )

    bucketed = df["category_count"].apply(lambda n: "4+" if n >= 4 else str(n))
    counts = bucketed.value_counts().reindex(["0", "1", "2", "3", "4+"], fill_value=0)

    fig, ax = plt.subplots(figsize=(7, 5))
    counts.plot(kind="bar", ax=ax, color="#8172B2", edgecolor="white")
    ax.set_title("Category Count Distribution per Review", fontsize=14, fontweight="bold")
    ax.set_xlabel("Number of Categories Assigned")
    ax.set_ylabel("Number of Reviews")
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "category_count_distribution.png", dpi=150)
    plt.close(fig)
    print("Saved: outputs/figures/category_count_distribution.png")


if __name__ == "__main__":
    print(f"Reading: {INPUT_PATH}")
    df = load_data()
    print(f"Total reviews: {len(df)}")

    plot_category_distribution(df)
    plot_rating_distribution(df)
    plot_monthly_review_count(df)
    plot_category_count_distribution(df)

    print("\nAll figures saved to outputs/figures/")
