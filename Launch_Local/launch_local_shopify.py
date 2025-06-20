# launch_local_shopify.py

import os
from dotenv import load_dotenv

# Yeni: shopify.env dosyasının bulunduğu dizini açıkça belirtiyoruz
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.envs', 'shopify.env')
load_dotenv(dotenv_path)

SHOPIFY_ACCOUNTS = [
    {
        "SHOPIFY_DOMAIN": os.getenv("SHOPIFY_DOMAIN"),
        "SHOPIFY_API_KEY": os.getenv("SHOPIFY_API_KEY"),
        "SHOPIFY_API_SECRET_KEY": os.getenv("SHOPIFY_API_SECRET_KEY"),
        "SHOPIFY_API_ACCESS_TOKEN": os.getenv("SHOPIFY_API_ACCESS_TOKEN")
    }
    # İstersen buraya daha fazla hesap ekleyebilirsin
]

# Bu yapı Config/config_shopify.py içinde import edilerek kullanılır:
# from launch_local import SHOPIFY_ACCOUNTS
