# config_github.py

import os

try:
    # Lokal ortamda .envs/github.env dosyasını kullanır
    from Launch_Local.launch_local_openai import GITHUB_ACCOUNTS
except ImportError:
    # Sunucu/GitHub ortamında environment variable'lardan alır
    # GitHub Secrets'a tanımlanmış tüm değişkenleri oku
    GITHUB_ACCOUNTS = [
        {
            "GIT_TOKEN_ID": os.getenv("GIT_TOKEN_ID"),
        }
        # Diğer hesaplar gerekiyorsa buraya eklenebilir
    ]
    