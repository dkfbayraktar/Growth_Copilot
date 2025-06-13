# fetch_meta_normalized_daily_to_json.py

import os
import pandas as pd
from datetime import datetime, timedelta

# Parquet dosyasının yolu
NORMALIZED_PATH = os.path.join(os.path.dirname(__file__), 'Data', 'API_Data', 'Meta', 'meta_normalized_daily.parquet')

# JSON dosyalarının yazılacağı yol
JSON_DAILY_DIR = os.path.join(os.path.dirname(__file__), 'Data', 'GPT_Friendly', 'Meta')
os.makedirs(JSON_DAILY_DIR, exist_ok=True)

def main():
    if not os.path.exists(NORMALIZED_PATH):
        print("Parquet dosyası bulunamadı. İşlem durduruldu.")
        return

    df = pd.read_parquet(NORMALIZED_PATH)
    if df.empty or 'veri_tarihi' not in df.columns:
        print("Parquet dosyası boş veya 'veri_tarihi' kolonunu içermiyor.")
        return

    df['veri_tarihi'] = pd.to_datetime(df['veri_tarihi']).dt.date

    today = datetime.now().date()
    check_date = today - timedelta(days=1)

    # JSON dosyaları zaten varsa
    existing_json_dates = {
        f.name.replace("meta_normalized_", "").replace(".json", "")
        for f in os.scandir(JSON_DAILY_DIR) if f.is_file() and f.name.endswith(".json")
    }

    # Parquet dosyasındaki tüm günleri al
    all_dates = df['veri_tarihi'].unique()

    for date in sorted(all_dates):
        date_str = date.strftime("%Y-%m-%d")

        # Eğer dosya zaten varsa ve son gün değilse atla
        if date_str in existing_json_dates and date != check_date:
            continue

        json_path = os.path.join(JSON_DAILY_DIR, f"meta_normalized_{date_str}.json")

        # Dosya varsa sil
        if os.path.exists(json_path):
            os.remove(json_path)

        df_day = df[df['veri_tarihi'] == date]
        df_day.to_json(json_path, orient='records', date_format='iso', force_ascii=False)
        print(f"JSON dosyası yazıldı: {json_path}")

if __name__ == "__main__":
    main()
