import os

# Shopify API Token (örnek)
SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
SHOPIFY_API_SECRET = os.getenv('SHOPIFY_API_SECRET')

# Meta Marketing API Token (örnek)
META_MARKETING_TOKEN = os.getenv('META_MARKETING_TOKEN')

# Meta Insights API Token (örnek)
META_INSIGHTS_TOKEN = os.getenv('META_INSIGHTS_TOKEN')

# OpenAI API Token (örnek)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Eğer birden fazla Shopify hesabı varsa, ikinci hesabın token'ları aşağıdaki gibi eklenebilir:
# SHOPIFY_API_KEY_2 = os.getenv('SHOPIFY_API_KEY_2')
# SHOPIFY_API_SECRET_2 = os.getenv('SHOPIFY_API_SECRET_2')

# Eğer birden fazla Meta Ad Account için token kullanacaksanız, aşağıdaki satırları açıp kullanabilirsiniz:
# META_MARKETING_TOKEN_2 = os.getenv('META_MARKETING_TOKEN_2')
# META_INSIGHTS_TOKEN_2 = os.getenv('META_INSIGHTS_TOKEN_2') 