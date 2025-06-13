import os

# Shopify Mağaza Domain ve Token bilgileri
SHOPIFY_STORES = [
    {
        "domain": "www.thenichebox.co",
        "access_token": os.getenv('SHOPIFY_API_ACCESS_TOKEN')
    },
    # Daha fazla mağaza eklemek için aşağıdaki örneği kullanın:
    # {
    #     "domain": "your-second-store.myshopify.com",
    #     "access_token": os.getenv('SHOPIFY_API_ACCESS_TOKEN_2')
    # },
] 