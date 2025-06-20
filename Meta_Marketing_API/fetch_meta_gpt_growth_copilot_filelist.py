# fetch_meta_gpt_growth_copilot_filelist.py

import os
import json
from datetime import datetime

# Klasör yapısı
DATA_FOLDER = "Data/GPT_Friendly/Meta"
MANIFEST_FOLDER = "Data/GPT_Friendly/Meta_Manifest"
ARCHIVE_FOLDER = os.path.join(MANIFEST_FOLDER, "Archive")
MANIFEST_FILENAME = "gpt_growth_copilot_meta_filelist.json"

# Çıktı dosyası (ana manifest)
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), MANIFEST_FOLDER, MANIFEST_FILENAME)


def generate_metadata():
    local_path = os.path.join(os.path.dirname(__file__), DATA_FOLDER)
    if not os.path.exists(local_path):
        print(f"Klasör bulunamadı: {local_path}")
        return

    # .json dosyalarının isimlerini topla
    json_files = sorted([
        f for f in os.listdir(local_path)
        if f.endswith(".json")
    ])

    if not json_files:
        print("Uyarı: Hiçbir .json dosyası bulunamadı, boş bir manifest oluşturuluyor.")

    metadata = {
        "version": "1.0",
        "type": "file_list",
        "files": json_files
    }

    # Manifest ve arşiv klasörlerini oluştur
    manifest_path = os.path.join(os.path.dirname(__file__), MANIFEST_FOLDER)
    archive_path = os.path.join(os.path.dirname(__file__), ARCHIVE_FOLDER)
    os.makedirs(manifest_path, exist_ok=True)
    os.makedirs(archive_path, exist_ok=True)

    # JSON olarak yaz (latest versiyon)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    print(f"✅ Metadata dosyası oluşturuldu: {OUTPUT_PATH}")

    # Tarih damgalı arşiv dosyasını yaz
    date_str = datetime.now().strftime("%Y-%m-%d")
    archive_file = f"gpt_growth_copilot_meta_filelist_{date_str}.json"
    archive_output_path = os.path.join(archive_path, archive_file)
    with open(archive_output_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    print(f"🗃️ Arşiv dosyası oluşturuldu: {archive_output_path}")


if __name__ == "__main__":
    generate_metadata()
