import os
import requests
from retry import retry

from gcc_utils import gccPrint

COVALENT_API_KEY = os.getenv("COVALENT_API_KEY", "")


def _parseCovalentResponse(response, tag):
    if response["error"] is False:
        return response["data"]

    error_message = response["error_message"]
    raise Exception(
        (f"{tag} Error") if error_message is None else (f"{tag} {error_message}")
    )


@retry((Exception), delay=10, tries=5)
def getPools():
    TAG = "[Covalent::getPools]"
    endpoint = f"https://api.covalenthq.com/v1/1313161554/xy=k/trisolaris/pools/?quote-currency=USD&format=JSON&key={COVALENT_API_KEY}"
    result = []
    try:
        response = requests.get(endpoint).json()
        data = _parseCovalentResponse(response, TAG)

        result = data["items"]
    except Exception as e:
        gccPrint(f"{TAG}: Error fetching pools: {e}", "ERROR")

    return result


@retry((Exception), delay=10, tries=5)
def getPool(address):
    TAG = "[Covalent::getPool]"
    endpoint = f"https://api.covalenthq.com/v1/1313161554/xy=k/trisolaris/pools/address/{address}/?quote-currency=USD&format=JSON&key={COVALENT_API_KEY}"
    result = None
    try:
        response = requests.get(endpoint).json()
        data = _parseCovalentResponse(response, TAG)

        if len(data["items"]) > 0:
            result = data["items"][0]
    except Exception as e:
        gccPrint(f"{TAG} Error fetching pool: {e}", "ERROR")

    return result
