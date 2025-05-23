# Shopify Admin API'den veri çekmek için script

# Buraya veri çekme fonksiyonları eklenecek 

import json
import os
from datetime import datetime
from config import SHOPIFY_API_KEY, SHOPIFY_API_SECRET

# İkinci hesap için environment variable'ı dinamik olarak oku
SHOPIFY_API_KEY_2 = os.getenv('SHOPIFY_API_KEY_2')
SHOPIFY_API_SECRET_2 = os.getenv('SHOPIFY_API_SECRET_2')

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'Data', 'Shopify_Data.json')

def fetch_and_save_shopify_data():
    accounts = [(SHOPIFY_API_KEY, SHOPIFY_API_SECRET)]
    # İkinci hesap varsa ekle
    if 'SHOPIFY_API_KEY_2' in globals() and SHOPIFY_API_KEY_2 and SHOPIFY_API_SECRET_2:
        accounts.append((SHOPIFY_API_KEY_2, SHOPIFY_API_SECRET_2))
    all_data = []
    for idx, (api_key, api_secret) in enumerate(accounts, 1):
        # Burada gerçek API çağrısı yapılacak, şimdilik örnek veri
        data = {
            "veri_tarihi": datetime.now().strftime('%Y-%m-%d'),
            "shopify_account_index": idx,
            "order_count": 12 * idx,
            "total_sales": 1500.75 * idx,
            "customer_count": 8 * idx,
            "conversion_rate": 2.3
        }
        all_data.append(data)
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"Shopify verisi kaydedildi: {DATA_PATH}")

if __name__ == "__main__":
    fetch_and_save_shopify_data() 