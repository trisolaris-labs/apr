import os
import requests
from web3 import Web3
from gcc_utils import gccPrint

TAG = "[TOP_POOLS_BASE] "

COVALENT_API_KEY = os.getenv("COVALENT_API_KEY", "")
COVALENT_ENDPOINT = f"https://api.covalenthq.com/v1/1313161554/xy=k/trisolaris/pools/?quote-currency=USD&format=JSON&key={COVALENT_API_KEY}"

def top_pools_base():
    gccPrint(TAG + "Starting")

    response = requests.get(COVALENT_ENDPOINT).json()
    pools = response['data']['items']

    top_pool_tokens = []
    for pool in pools:
        if pool['fee_24h_quote'] >= 1:
            token0 = Web3.toChecksumAddress(pool['token_0']['contract_address'])
            token1 = Web3.toChecksumAddress(pool['token_1']['contract_address'])
            top_pool_tokens.append([token0, token1])

    return top_pool_tokens


if __name__ == "__main__":
    top_pools_base()
