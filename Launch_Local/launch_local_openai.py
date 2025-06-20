# launch_local_openai.py

import os
from dotenv import load_dotenv

# Yeni: meta.env dosyasının bulunduğu dizini açıkça belirtiyoruz
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.envs', 'openai.env')
load_dotenv(dotenv_path)

OPENAI_ACCOUNTS = [
    {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    }
    # İstersen buraya daha fazla hesap ekleyebilirsin
]

# Bu yapı Config/config_Oopenai.py içinde import edilerek kullanılır:
# from launch_local import OPENAI_ACCOUNTS