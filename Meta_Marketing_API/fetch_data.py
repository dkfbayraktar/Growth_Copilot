# Meta Marketing API'den veri çekmek için script

import json
import os
from datetime import datetime
from config import META_MARKETING_TOKEN

# İkinci hesap için environment variable'ı dinamik olarak oku
META_MARKETING_TOKEN_2 = os.getenv('META_MARKETING_TOKEN_2')

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'Data', 'Meta_Marketing_Data.json')

def fetch_and_save_meta_marketing_data():
    tokens = [META_MARKETING_TOKEN]
    # İkinci token varsa ekle
    if META_MARKETING_TOKEN_2:
        tokens.append(META_MARKETING_TOKEN_2)
    all_data = []
    for idx, token in enumerate(tokens, 1):
        # Burada gerçek API çağrısı yapılacak, şimdilik örnek veri
        data = {
            "veri_tarihi": datetime.now().strftime('%Y-%m-%d'),
            "ad_account_index": idx,
            "ad_spend": 500.0 * idx,
            "impressions": 12000 * idx,
            "clicks": 350 * idx,
            "cpc": 1.43
        }
        all_data.append(data)
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"Meta Marketing verisi kaydedildi: {DATA_PATH}")

if __name__ == "__main__":
    fetch_and_save_meta_marketing_data()

# Buraya veri çekme fonksiyonları eklenecek 