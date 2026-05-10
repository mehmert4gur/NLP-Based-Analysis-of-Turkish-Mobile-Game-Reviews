from google_play_scraper import reviews, Sort
import pandas as pd
from tqdm import tqdm
import time
from pathlib import Path

from local_games import LOCAL_GAMES


RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def fetch_reviews_for_game(app_id, game_name, developer, sort_type, sort_name, review_count=1000):
    """
    Tek bir oyun için Google Play yorumlarını çeker.
    """

    result, _ = reviews(
        app_id,
        lang="tr",
        country="tr",
        sort=sort_type,
        count=review_count
    )

    rows = []

    for r in result:
        rows.append({
            "review_id": r.get("reviewId"),
            "developer": developer,
            "game_name": game_name,
            "app_id": app_id,
            "content": r.get("content"),
            "rating": r.get("score"),
            "thumbs_up_count": r.get("thumbsUpCount"),
            "review_created_at": r.get("at"),
            "review_source_sort": sort_name,
            "user_name": r.get("userName"),
            "developer_reply": r.get("replyContent"),
            "developer_replied_at": r.get("repliedAt")
        })

    return rows


def collect_all_reviews(review_count_per_sort=1000):
    """
    Tüm oyunlar için yorumları çeker.
    Her oyun için:
    - NEWEST
    - MOST_RELEVANT
    olmak üzere iki farklı sıralamadan veri toplar.
    """

    all_rows = []

    sort_options = [
        {
            "sort_type": Sort.NEWEST,
            "sort_name": "newest"
        },
        {
            "sort_type": Sort.MOST_RELEVANT,
            "sort_name": "most_relevant"
        }
    ]

    for game in tqdm(LOCAL_GAMES, desc="Oyunlar işleniyor"):
        app_id = game["app_id"]
        game_name = game["name"]
        developer = game["developer"]

        for sort_option in sort_options:
            sort_type = sort_option["sort_type"]
            sort_name = sort_option["sort_name"]

            try:
                print(f"\nÇekiliyor: {developer} - {game_name} - {sort_name}")

                rows = fetch_reviews_for_game(
                    app_id=app_id,
                    game_name=game_name,
                    developer=developer,
                    sort_type=sort_type,
                    sort_name=sort_name,
                    review_count=review_count_per_sort
                )

                all_rows.extend(rows)

                print(f"{len(rows)} yorum çekildi.")

                time.sleep(1)

            except Exception as e:
                print(f"HATA: {developer} - {game_name} - {app_id} - {sort_name}")
                print(e)
                continue

    df = pd.DataFrame(all_rows)

    if df.empty:
        return df

    before_count = len(df)

    df = df.drop_duplicates(subset=["review_id"])

    after_count = len(df)

    print("\nToplam çekilen yorum:", before_count)
    print("Tekrarlar silindikten sonra:", after_count)
    print("Silinen tekrar sayısı:", before_count - after_count)

    return df


if __name__ == "__main__":
    df = collect_all_reviews(review_count_per_sort=1000)

    excel_path = RAW_DATA_DIR / "yerel_oyun_yorumlari.xlsx"
    csv_path = RAW_DATA_DIR / "yerel_oyun_yorumlari.csv"

    import re
    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

    # Remove illegal characters for Excel export
    for col in df.select_dtypes(['object', 'string']).columns:
        df[col] = df[col].apply(lambda x: ILLEGAL_CHARACTERS_RE.sub("", str(x)) if pd.notna(x) else x)

    df.to_excel(excel_path, index=False)
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print("\nDosyalar kaydedildi:")
    print(excel_path)
    print(csv_path)