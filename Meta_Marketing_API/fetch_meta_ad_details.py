# fetch_meta_ad_details.py

import os
import sys
import pandas as pd
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Config.config_meta import META_ACCOUNTS
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'Data', 'API_Data', 'Meta', 'meta_ad_details.parquet')

def fetch_and_save_ad_details():
    if os.path.exists(DATA_PATH):
        df_existing = pd.read_parquet(DATA_PATH)
        existing_ad_ids = set(df_existing['ad_id'].unique())
    else:
        df_existing = pd.DataFrame()
        existing_ad_ids = set()

    today = datetime.now().date()
    start_date = datetime(2025, 6, 1).date()
    check_date = today - timedelta(days=1)

    all_data = []

    for account_config in META_ACCOUNTS:
        current_account_id = account_config['META_ACCOUNT_ID']
        current_token = account_config['META_MARKETING_TOKEN']
        app_id = account_config['META_APP_ID']
        app_secret = account_config['META_APP_SECRET']

        FacebookAdsApi.init(app_id=app_id, app_secret=app_secret, access_token=current_token)

        if df_existing.empty:
            ad_filter_date = start_date
            date_range = (check_date - start_date).days + 1
        else:
            ad_filter_date = check_date
            date_range = 1

        for i in range(date_range):
            query_date = (ad_filter_date + timedelta(days=i)).strftime('%Y-%m-%d')
            print(f"Fetching ad data for date: {query_date}")

            account = AdAccount(f'act_{current_account_id}')
            insights = account.get_insights(fields=['ad_id', 'quality_ranking', 'engagement_rate_ranking', 'conversion_rate_ranking'], params={
                'time_range': {'since': query_date, 'until': query_date},
                'level': 'ad'
            })

            ad_id_set = {entry.get('ad_id') for entry in insights if entry.get('ad_id') and entry.get('ad_id') not in existing_ad_ids}

            for ad_id in ad_id_set:
                try:
                    ad_object = Ad(ad_id)
                    ad_detail = ad_object.api_get(fields=[
                        'id', 'name', 'adcreatives', 'effective_status', 'status',
                        'created_time', 'updated_time', 'page_id', 'instagram_actor_id',
                        'adlabels', 'object_type', 'ad_format', 'destination_type',
                        'dynamic_ad_voice', 'asset_feed_spec', 'template_data',
                        'creative'
                    ])

                    # Get ranking metrics for this ad
                    ad_insights = next((insight for insight in insights if insight.get('ad_id') == ad_id), {})
                    
                    ad_data = {
                        'ad_id': ad_detail.get('id', ''),
                        'ad_name': ad_detail.get('name', ''),
                        'name': ad_detail.get('name', ''),
                        'effective_status': ad_detail.get('effective_status', ''),
                        'ad_status': ad_detail.get('status', ''),
                        'page_id': ad_detail.get('page_id', ''),
                        'instagram_actor_id': ad_detail.get('instagram_actor_id', ''),
                        'adlabels': ad_detail.get('adlabels', ''),
                        'object_type': ad_detail.get('object_type', ''),
                        'ad_format': ad_detail.get('ad_format', ''),
                        'destination_type': ad_detail.get('destination_type', ''),
                        'dynamic_ad_voice': ad_detail.get('dynamic_ad_voice', ''),
                        'asset_feed_spec': ad_detail.get('asset_feed_spec', ''),
                        'template_data': ad_detail.get('template_data', ''),
                        'creative_id': ad_detail.get('creative', {}).get('id', ''),
                        'quality_ranking': ad_insights.get('quality_ranking', ''),
                        'engagement_rate_ranking': ad_insights.get('engagement_rate_ranking', ''),
                        'conversion_rate_ranking': ad_insights.get('conversion_rate_ranking', '')
                    }

                    creative_id = ad_data['creative_id']
                    if creative_id:
                        creative = AdCreative(creative_id).api_get(fields=[
                            'title', 'body', 'image_url', 'thumbnail_url',
                            'link_url', 'object_story_spec', 'call_to_action_type',
                            'call_to_action'
                        ])

                        try:
                            link_url_domain = creative.get('link_url', '').split('/')[2]
                        except:
                            link_url_domain = ''

                        ad_data.update({
                            'title': creative.get('title', ''),
                            'body': creative.get('body', ''),
                            'headline': creative.get('title', ''),
                            'image_url': creative.get('image_url', ''),
                            'thumbnail_url': creative.get('thumbnail_url', ''),
                            'link_url': creative.get('link_url', ''),
                            'link_url_domain': link_url_domain,
                            'call_to_action_type': creative.get('call_to_action_type', ''),
                            'call_to_action.value.link_caption': creative.get('call_to_action', {}).get('value', {}).get('link_caption', ''),
                            'object_story_spec.message': creative.get('object_story_spec', {}).get('message', ''),
                            'object_story_spec.link_data.description': creative.get('object_story_spec', {}).get('link_data', {}).get('description', ''),
                            'object_story_spec.link_data.caption': creative.get('object_story_spec', {}).get('link_data', {}).get('caption', ''),
                            'video_data.video_id': creative.get('video_data', {}).get('video_id', '')
                        })

                    all_data.append(ad_data)

                except Exception as e:
                    print(f"Error processing ad {ad_id}: {e}")
                    continue

    if all_data:
        df_new = pd.DataFrame(all_data)

        if not df_existing.empty:
            compare_cols = ['ad_id', 'ad_status', 'creative_id']
            df_latest = df_new[compare_cols].copy()
            df_existing_subset = df_existing[compare_cols].drop_duplicates('ad_id', keep='last')

            df_merged = df_latest.merge(df_existing_subset, on='ad_id', how='left', suffixes=('', '_prev'))

            df_new['status_changed'] = df_merged['ad_status'] != df_merged['ad_status_prev']
            df_new['creative_changed'] = df_merged['creative_id'] != df_merged['creative_id_prev']
        else:
            df_new['status_changed'] = False
            df_new['creative_changed'] = False

        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_parquet(DATA_PATH, index=False)
        print(f"Meta ad details data updated: {DATA_PATH}")
    else:
        print("No new ad details data found.")

if __name__ == "__main__":
    fetch_and_save_ad_details()
