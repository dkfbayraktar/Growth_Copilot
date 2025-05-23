# Meta Insights API'den veri çekmek için script

# Buraya veri çekme fonksiyonları eklenecek 

import json
import os
from datetime import datetime
from config import META_INSIGHTS_TOKEN

# İkinci hesap için environment variable'ı dinamik olarak oku
META_INSIGHTS_TOKEN_2 = os.getenv('META_INSIGHTS_TOKEN_2')

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'Data', 'Meta_Insights_Data.json')

def fetch_and_save_meta_insights_data():
    tokens = [META_INSIGHTS_TOKEN]
    # İkinci token varsa ekle
    if META_INSIGHTS_TOKEN_2:
        tokens.append(META_INSIGHTS_TOKEN_2)
    all_data = []
    for idx, token in enumerate(tokens, 1):
        # Burada gerçek API çağrısı yapılacak, şimdilik örnek veri
        data = {
            "veri_tarihi": datetime.now().strftime('%Y-%m-%d'),
            "ad_account_index": idx,
            "reach": 8000 * idx,
            "engagement": 1200 * idx,
            "followers": 3500 * idx
        }
        all_data.append(data)
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"Meta Insights verisi kaydedildi: {DATA_PATH}")

if __name__ == "__main__":
    fetch_and_save_meta_insights_data() 