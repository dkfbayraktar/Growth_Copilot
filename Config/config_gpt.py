# config_gpt.py

import os

try:
    # Lokal ortamda .envs/gpt.env dosyasını kullanır
    from Launch_Local.launch_local_gpt import CUSTOM_GPTS
except ImportError:
    # Sunucu/GitHub ortamında environment variable'lardan alır
    # GitHub Secrets'a tanımlanmış tüm değişkenleri oku
    CUSTOM_GPTS = [
        {
            "GPT_Growth_Copilot_ID": os.getenv("GPT_Growth_Copilot_ID"),
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")
        }
        # Diğer hesaplar gerekiyorsa buraya eklenebilir
    ]
    