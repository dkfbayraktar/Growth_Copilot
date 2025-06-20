# launch_local_github.py

import os
from dotenv import load_dotenv

# Yeni: github.env dosyasının bulunduğu dizini açıkça belirtiyoruz
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.envs', 'github.env')
load_dotenv(dotenv_path)

GITHUB_ACCOUNTS = [
    {
        "GIT_TOKEN_ID": os.getenv("GIT_TOKEN_ID"),
    }
    # İstersen buraya daha fazla hesap ekleyebilirsin
]

# Bu yapı Config/config_github.py içinde import edilerek kullanılır:
# from launch_local import GITHUB_ACCOUNTS
