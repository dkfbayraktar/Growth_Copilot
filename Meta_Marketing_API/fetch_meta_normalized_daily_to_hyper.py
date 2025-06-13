# fetch_meta_normalized_daily_to_hyper.py

import os
import sys
import subprocess
import pandas as pd
from datetime import datetime, timedelta

# Hyper API yüklemesi (gerekiyorsa)
try:
    from tableauhyperapi import HyperProcess, Connection, TableDefinition, SqlType, Telemetry, Inserter, CreateMode, TableName
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tableauhyperapi==0.0.22106"])
    from tableauhyperapi import HyperProcess, Connection, TableDefinition, SqlType, Telemetry, Inserter, CreateMode, TableName

# Dosya yolları
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'Data', 'API_Data', 'Meta')
PARQUET_FILE = os.path.join(DATA_DIR, 'meta_normalized_daily.parquet')
HYPER_FILE = os.path.join(DATA_DIR, 'meta_normalized_daily.hyper')

# Hedef tarih: bir önceki gün
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

# Parquet dosyasından veri oku
if not os.path.exists(PARQUET_FILE):
    print("Parquet dosyası bulunamadı. İşlem sonlandırıldı.")
    sys.exit()

df = pd.read_parquet(PARQUET_FILE)

# Eğer veri boşsa veya ilgili gün verisi yoksa çık
if df.empty:
    print("Parquet dosyası boş.")
    sys.exit()

df['date_start'] = pd.to_datetime(df['date_start']).dt.strftime('%Y-%m-%d')
df_yesterday = df[df['date_start'] == yesterday]

if df_yesterday.empty:
    print(f"{yesterday} tarihine ait veri yok.")
    sys.exit()

# Hyper işlemini başlat
with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    with Connection(endpoint=hyper.endpoint, database=HYPER_FILE, create_mode=CreateMode.CREATE_IF_NOT_EXISTS) as connection:

        table_name = TableName("Meta", "NormalizedDaily")

        # İlk seferde tabloyu oluştur
        if not connection.catalog.has_table(table_name):
            table_definition = TableDefinition(
                table_name=table_name,
                columns=[(col, SqlType.text()) for col in df_yesterday.columns]
            )
            connection.catalog.create_table(table_definition)

        else:
            # Eğer aynı güne ait veri varsa, onu sil
            connection.execute_command(f"DELETE FROM {table_name} WHERE date_start = '{yesterday}'")

        # Yeni verileri ekle
        with Inserter(connection, table_name) as inserter:
            inserter.add_rows(rows=df_yesterday.values.tolist())
            inserter.execute()

print(f"{yesterday} tarihli veriler .hyper dosyasına başarıyla eklendi.")
