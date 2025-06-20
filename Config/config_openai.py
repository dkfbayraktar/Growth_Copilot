# config_openai.py

import os

try:
    # Lokal ortamda .envs/openai.env dosyasını kullanır
    from Launch_Local.launch_local_openai import OPENAI_ACCOUNTS
except ImportError:
    # Sunucu/GitHub ortamında environment variable'lardan alır
    # GitHub Secrets'a tanımlanmış tüm değişkenleri oku
    OPENAI_ACCOUNTS = [
        {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        }
        # Diğer hesaplar gerekiyorsa buraya eklenebilir
    ]
    
