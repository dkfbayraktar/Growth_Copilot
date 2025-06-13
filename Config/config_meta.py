# config_meta.py

import os

try:
    # Lokal ortamda .envs/meta.env dosyasını kullanır
    from Launch_Local.launch_local_meta import META_ACCOUNTS
except ImportError:
    # Sunucu/GitHub ortamında environment variable'lardan alır
    # GitHub Secrets'a tanımlanmış tüm değişkenleri oku
    META_ACCOUNTS = [
        {
            "META_ACCOUNT_ID": os.getenv("META_ACCOUNT_ID"),
            "META_MARKETING_TOKEN": os.getenv("META_MARKETING_TOKEN"),
            "META_APP_ID": os.getenv("META_APP_ID"),
            "META_APP_SECRET": os.getenv("META_APP_SECRET")
        }
        # Diğer hesaplar gerekiyorsa buraya eklenebilir
    ]
