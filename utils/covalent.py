import os
import requests
from retry import retry

COVALENT_API_KEY = os.getenv("COVALENT_API_KEY", "")
COVALENT_ENDPOINT = f"https://api.covalenthq.com/v1/1313161554/xy=k/trisolaris/pools/?quote-currency=USD&format=JSON&key={COVALENT_API_KEY}"

@retry((Exception), delay=10, tries=5)
def getPools():
    pools = []
    try:
        response = requests.get(COVALENT_ENDPOINT).json()
        pools = response['data']['items']
    except Exception as e:
        raise e

    return pools
