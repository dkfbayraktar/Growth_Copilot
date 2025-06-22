# fetch_meta_normalized_daily.py

import os
import pandas as pd
from datetime import datetime

# Veri yolları
DEMOGRAPHIC_PATH = os.path.join(os.path.dirname(__file__), 'Data', 'API_Data', 'Meta', 'meta_demographic_daily.parquet')
PERFORMANCE_PATH = os.path.join(os.path.dirname(__file__), 'Data', 'API_Data', 'Meta', 'meta_performance_daily.parquet')
AD_DETAILS_PATH = os.path.join(os.path.dirname(__file__), 'Data', 'API_Data', 'Meta', 'meta_ad_details.parquet')
NORMALIZED_PATH = os.path.join(os.path.dirname(__file__), 'Data', 'API_Data', 'Meta', 'meta_normalized_daily.parquet')

# Normalize edilecek metrikler (manuel hesaplananlar hariç)
all_kpi_columns = [
    'impressions', 'reach', 'clicks', 'unique_clicks',
    'spend', 'page_view', 'add_to_cart', 'initiate_checkout',
    'purchase', 'result', 'purchase_conversion_value'
]

identity_columns = [
    'veri_tarihi', 'ad_id', 'ad_name', 'adset_id', 'adset_name',
    'campaign_id', 'campaign_name', 'account_id', 'account_name', 'breakdown_type'
]

breakdown_columns = ['age', 'gender', 'country', 'region', 'publisher_platform']

def normalize_demographic_kpi():
    if not os.path.exists(DEMOGRAPHIC_PATH) or not os.path.exists(PERFORMANCE_PATH):
        print("Gerekli veri dosyaları bulunamadı.")
        return

    df_demo = pd.read_parquet(DEMOGRAPHIC_PATH)
    df_perf = pd.read_parquet(PERFORMANCE_PATH)

    # AD details dosyasını yükle
    if os.path.exists(AD_DETAILS_PATH):
        df_ad_details = pd.read_parquet(AD_DETAILS_PATH)
    else:
        print("Ad Details dosyası bulunamadı.")
        return

    normalized_rows = []
    today = datetime.now().date()

    for (veri_tarihi, ad_id), group in df_demo.groupby(['veri_tarihi', 'ad_id']):
        df_agg = df_perf[
            (df_perf['veri_tarihi'] == veri_tarihi) & (df_perf['ad_id'] == ad_id)
        ]
        if df_agg.empty:
            continue

        total_values = df_agg.iloc[0]

        # first_seen_date, last_seen_date, duration (days) metriklerini ekle
        for extra_col in ['first_seen_date', 'last_seen_date', 'duration (days)']:
            if extra_col in df_perf.columns:
                total_values[extra_col] = df_perf[df_perf['ad_id'] == ad_id][extra_col].iloc[0]

        for idx, row in group.iterrows():
            ratio_row = {}
            for col in all_kpi_columns:
                total_val = total_values.get(col, 0)
                partial_val = row.get(col, 0)
                ratio = partial_val / group[col].sum() if group[col].sum() != 0 else 0
                ratio_row[col] = ratio * total_val

            base_info = {col: row[col] for col in identity_columns if col in row}
            breakdown_info = {col: row[col] for col in breakdown_columns if col in row and pd.notna(row[col])}

            full_row = {**base_info, **breakdown_info, **ratio_row}

            for extra_col in ['first_seen_date', 'last_seen_date', 'duration (days)']:
                if extra_col in total_values:
                    full_row[extra_col] = total_values[extra_col]

            # AD details bilgilerini eşleştir (sadece olmayanları ekle)
            if ad_id in df_ad_details['ad_id'].values:
                ad_info = df_ad_details[df_ad_details['ad_id'] == ad_id].iloc[0].to_dict()
                for key, val in ad_info.items():
                    if key not in full_row:
                        full_row[key] = val

            

                # Satır bazlı KPI'ları hesapla ve ekle (en son işlem olarak uygulanır)
    full_row['row_ctr'] = full_row['clicks'] / full_row['impressions'] if full_row['impressions'] else 0
    full_row['row_cpc'] = full_row['spend'] / full_row['clicks'] if full_row['clicks'] else 0
    full_row['row_cpm'] = (full_row['spend'] / full_row['impressions']) * 1000 if full_row['impressions'] else 0
    full_row['row_roas'] = full_row['purchase_conversion_value'] / full_row['spend'] if full_row['spend'] else 0
    full_row['row_cvr'] = full_row['purchase'] / full_row['clicks'] if full_row['clicks'] else 0
    full_row['row_cvr_funnel'] = (full_row['purchase'] + full_row['add_to_cart'] + full_row['initiate_checkout']) / full_row['clicks'] if full_row['clicks'] else 0
    full_row['row_purchase_funnel'] = full_row['purchase'] + full_row['add_to_cart'] + full_row['initiate_checkout']

    normalized_rows.append(full_row)

    df_normalized = pd.DataFrame(normalized_rows)
    df_normalized.to_parquet(NORMALIZED_PATH, index=False)
    print(f"Normalize edilmiş dosya kaydedildi: {NORMALIZED_PATH}")

if __name__ == "__main__":
    normalize_demographic_kpi()
