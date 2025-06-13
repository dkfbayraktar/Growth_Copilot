# launch_local_meta.py

import os
from dotenv import load_dotenv

# Yeni: meta.env dosyasının bulunduğu dizini açıkça belirtiyoruz
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.envs', 'meta.env')
load_dotenv(dotenv_path)

META_ACCOUNTS = [
    {
        "META_ACCOUNT_ID": os.getenv("META_ACCOUNT_ID"),
        "META_MARKETING_TOKEN": os.getenv("META_MARKETING_TOKEN"),
        "META_APP_ID": os.getenv("META_APP_ID"),
        "META_APP_SECRET": os.getenv("META_APP_SECRET")
    }
    # İstersen buraya daha fazla hesap ekleyebilirsin
]

# Bu yapı Config/config_meta.py içinde import edilerek kullanılır:
# from launch_local import META_ACCOUNTS
