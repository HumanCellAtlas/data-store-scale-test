from random import choice

def get_replica():
    return choice(['aws','gcp'])

ASYNC_COPY_THRESHOLD = 64 * 1024 * 1024
STAGING_BUCKET = "dss-checkout-tsmith1"
