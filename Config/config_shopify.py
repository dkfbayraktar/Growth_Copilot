import os

# Shopify Mağaza Domain ve Token bilgileri
SHOPIFY_STORES = [
    {
        "SHOPIFY_DOMAIN": os.getenv("SHOPIFY_DOMAIN"),
        "SHOPIFY_API_KEY": os.getenv("SHOPIFY_API_KEY"),
        "SHOPIFY_API_SECRET_KEY": os.getenv("SHOPIFY_API_SECRET_KEY"),
        "SHOPIFY_API_ACCESS_TOKEN": os.getenv("SHOPIFY_API_ACCESS_TOKEN"),
    },
    # Daha fazla mağaza eklemek için aşağıdaki örneği kullanın:
    # {
    #     "SHOPIFY_DOMAIN_2": os.getenv("SHOPIFY_DOMAIN_2"),
    #     "SHOPIFY_API_KEY_2": os.getenv("SHOPIFY_API_KEY_2"),
    #     "SHOPIFY_API_SECRET_KEY_2": os.getenv("SHOPIFY_API_SECRET_KEY_2"),
    #     "SHOPIFY_API_ACCESS_TOKEN_2": os.getenv("SHOPIFY_API_ACCESS_TOKEN_2")
    # },
] 
