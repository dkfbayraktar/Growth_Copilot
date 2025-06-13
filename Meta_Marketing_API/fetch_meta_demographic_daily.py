# fetch_meta_demographic_daily.py

import os
import sys
import pandas as pd
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Config.config_meta import META_ACCOUNTS
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'Data', 'API_Data', 'Meta', 'meta_demographic_daily.parquet')

def fetch_and_save_meta_demographic_data():
    if os.path.exists(DATA_PATH):
        df_existing = pd.read_parquet(DATA_PATH)
        existing_dates = set(df_existing['veri_tarihi'].unique())
    else:
        df_existing = pd.DataFrame()
        existing_dates = set()

    today = datetime.now().date()
    start_date = datetime(2025, 6, 1).date()
    check_date = today - timedelta(days=1)

    if df_existing.empty:
        all_dates = {
            (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
            for i in range((check_date - start_date).days + 1)
        }
    else:
        all_dates = {check_date.strftime('%Y-%m-%d')}

    missing_dates = sorted(list(all_dates - existing_dates))
    all_data = []

    breakdown_sets = [
        (['age'], 'age'),
        (['gender'], 'gender'),
        (['country'], 'country'),
        (['region'], 'region'),
        (['publisher_platform'], 'platform')
    ]

    for account_config in META_ACCOUNTS:
        current_account_id = account_config['META_ACCOUNT_ID']
        current_token = account_config['META_MARKETING_TOKEN']
        app_id = account_config['META_APP_ID']
        app_secret = account_config['META_APP_SECRET']

        FacebookAdsApi.init(app_id=app_id, app_secret=app_secret, access_token=current_token)
        account = AdAccount(f'act_{current_account_id}')

        for date_str in missing_dates:
            for breakdown, breakdown_name in breakdown_sets:
                print(f"Veri çekiliyor: Account {current_account_id}, Tarih {date_str}, Breakdown: {breakdown_name}")

                params = {
                    'time_range': {'since': date_str, 'until': date_str},
                    'level': 'ad',
                    'fields': [
                        'ad_id', 'ad_name', 'adset_id', 'adset_name', 'campaign_id', 'campaign_name',
                        'account_id', 'account_name', 'impressions', 'reach', 'clicks',
                        'unique_clicks', 'spend'
                    ],
                    'breakdowns': breakdown,
                    'action_report_time': 'impression',
                    'actions': ['page_view', 'add_to_cart', 'initiate_checkout', 'purchase', 'result', 'purchase_conversion_value']
                }

                try:
                    ads = account.get_insights(
                        fields=params['fields'],
                        params={k: v for k, v in params.items() if k != 'fields'}
                    )
                except Exception as e:
                    print(f"Hata oluştu: {e} — Tarih: {date_str}, Account: {current_account_id}, Breakdown: {breakdown_name}")
                    continue

                for ad in ads:
                    try:
                        ad_data = {
                            "veri_tarihi": date_str,
                            "ad_account_index": META_ACCOUNTS.index(account_config) + 1,
                            "breakdown_type": breakdown_name,
                            "ad_id": ad.get("ad_id", ""),
                            "account_id": ad.get("account_id", ""),
                            "account_name": ad.get("account_name", ""),
                            "ad_name": ad.get("ad_name", ""),
                            "adset_id": ad.get("adset_id", ""),
                            "adset_name": ad.get("adset_name", ""),
                            "campaign_id": ad.get("campaign_id", ""),
                            "campaign_name": ad.get("campaign_name", ""),
                            "impressions": int(ad.get("impressions", 0)),
                            "reach": int(ad.get("reach", 0)),
                            "clicks": int(ad.get("clicks", 0)),
                            "unique_clicks": int(ad.get("unique_clicks", 0)),
                            "spend": float(ad.get("spend", 0.0))
                        }

                        for action in ad.get("actions", []):
                            action_type = action.get("action_type")
                            value = action.get("value", 0)
                            if action_type:
                                ad_data[action_type] = value

                        for key in breakdown:
                            ad_data[key] = ad.get(key, "")

                        all_data.append(ad_data)
                    except Exception as e:
                        print(f"Ad bazlı hata: {e} — Ad ID: {ad.get('ad_id', 'bilinmiyor')}")
                        continue

    if all_data:
        df_new = pd.DataFrame(all_data)

        # Remove old data for the same date to avoid duplication
        df_existing = df_existing[df_existing['veri_tarihi'] != pd.to_datetime(check_date)]
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)

        # KPI: ad_id bazında ilk ve son görünme günü ve duration
        df_combined['veri_tarihi'] = pd.to_datetime(df_combined['veri_tarihi'])
        first_seen = df_combined.groupby('ad_id')['veri_tarihi'].min().reset_index().rename(columns={'veri_tarihi': 'first_seen_date'})
        last_seen = df_combined.groupby('ad_id')['veri_tarihi'].max().reset_index().rename(columns={'veri_tarihi': 'last_seen_date'})

        df_combined = df_combined.merge(first_seen, on='ad_id', how='left')
        df_combined = df_combined.merge(last_seen, on='ad_id', how='left')
        df_combined['duration (days)'] = (df_combined['last_seen_date'] - df_combined['first_seen_date']).dt.days + 1

        df_combined.to_parquet(DATA_PATH, index=False)
        print(f"Demografik veri kaydedildi: {DATA_PATH}")
    else:
        print("Yeni veri bulunamadı. Dosya güncellenmedi.")

if __name__ == "__main__":
    fetch_and_save_meta_demographic_data()
