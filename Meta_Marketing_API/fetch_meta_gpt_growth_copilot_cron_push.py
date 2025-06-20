# fetch_meta_gpt_growth_copilot_cron_push.py

import os
import json
import requests
from datetime import datetime

# OpenAI GPT ID ve API Key bilgileri
try:
    from Config.config_gpt import CUSTOM_GPTS
    GPT_Growth_Copilot_ID = CUSTOM_GPTS[0]["GPT_Growth_Copilot_ID"]
    OPENAI_API_KEY = CUSTOM_GPTS[0]["OPENAI_API_KEY"]
except:
    GPT_Growth_Copilot_ID = os.getenv("GPT_Growth_Copilot_ID")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Manifest dosyasının yolu
MANIFEST_PATH = os.path.join(os.path.dirname(__file__), 'Data', 'GPT_Friendly', 'Meta_Manifest', 'gpt_growth_copilot_meta_filelist.json')

# Log dosyası dizini ve yolu
LOG_DIR = os.path.join(os.path.dirname(__file__), 'Logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'push_metadata_log.txt')

# OpenAI API endpoint
OPENAI_ENDPOINT = f"https://api.openai.com/v1/gpts/{GPT_Growth_Copilot_ID}"

# Headers
HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}


def push_metadata():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not os.path.exists(MANIFEST_PATH):
        msg = f"[{timestamp}] ❌ Manifest dosyası bulunamadı: {MANIFEST_PATH}"
        print(msg)
        with open(LOG_FILE, 'a', encoding='utf-8') as log:
            log.write(msg + "\n")
        return

    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    payload = {
        "files": metadata.get("files", [])
    }

    response = requests.patch(OPENAI_ENDPOINT, headers=HEADERS, json=payload)

    if response.status_code == 200:
        msg = f"[{timestamp}] ✅ GPT metadata başarıyla güncellendi. Dosya sayısı: {len(payload['files'])}"
    else:
        msg = f"[{timestamp}] ❌ Hata: {response.status_code} - {response.text}"

    print(msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as log:
        log.write(msg + "\n")


if __name__ == "__main__":
    push_metadata()
