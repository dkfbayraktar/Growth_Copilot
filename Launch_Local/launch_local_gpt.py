# launch_local_gpt.py

import os
from dotenv import load_dotenv

# Yeni: gpt.env dosyasının bulunduğu dizini açıkça belirtiyoruz
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.envs', 'gpt.env')
load_dotenv(dotenv_path)

CUSTOM_GPTS = [
    {
        "GPT_Growth_Copilot_ID": os.getenv("GPT_Growth_Copilot_ID"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")
    }
    # İstersen buraya daha fazla hesap ekleyebilirsin
]

# Bu yapı Config/config_gpt.py içinde import edilerek kullanılır:
# from launch_local import CUSTOM_GPTS
