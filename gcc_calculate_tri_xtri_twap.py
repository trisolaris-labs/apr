"""
This file is used for Google Cloud functions to:
    1. Maintain a list of historical prices for TRI and xTRI
    2. Update the TWAP price for TRI and xTRI
"""

import json
import os
from statistics import geometric_mean

from web3 import Web3

from gcc_utils import get_event_id, get_google_cloud_storage_blob
from utils.constants import TRI_ADDRESS, WNEAR_ADDRESS
from utils.node import init_tlp, w3
from utils.prices import getTriXTriRatio

# Output file name
FILE_NAME = "tri_xtri_twap.json"

# Google Cloud Storage
TRISOLARIS_PRICES_BUCKET = "trisolaris_public"
TRISOLARIS_PRICES_BUCKET_FILE_PATH = FILE_NAME
TRISOLARIS_TRI_XTRI_TWAP_DATA_FILE_PATH = "tri_xtri_historical_prices.json"

TAG = "[GCC_TRI_XTRI_TWAP]"

TLP_TRI_USDT = "0x61C9E05d1Cdb1b70856c7a2c53fA9c220830633c"
TLP_TRI_NEAR = "0x84b123875F0F36B966d0B6Ca14b31121bd9676AD"
TLP_NEAR_USDC = "0x20F8AeFB5697B77E0BB835A8518BE70775cdA1b0"
TLP_NEAR_USDT = "0x03B666f3488a7992b2385B12dF7f35156d7b29cD"
TRI_TOKEN_DECIMALS = 18
NEAR_TOKEN_DECIMALS = 24

# Number of items to keep in the price history
MAX_WINDOW_SIZE = 20
MAX_HISTORICAL_WINDOW_SIZE = 100

web3_url = os.getenv("AURORA_W3_URL", "https://mainnet.aurora.dev/")
w3 = Web3(Web3.HTTPProvider(web3_url))

# Calculates time weighted average price of TRI token
# Uploads historical prices to gcc file storage
# Uploads result to gcc file storage
def gcc_calculate_tri_xtri_twap(data, context):
    event_id = get_event_id(context)

    print(TAG + "Beginning Google Cloud Fn processing for event_id: {0}".format(event_id))

    (near_price_usd, tri_price_usd, xtri_price_usd) = get_prices()
    print(TAG + " weighted average NEAR price: ${0}".format(near_price_usd))
    print(TAG + " weighted average TRI price: ${0}".format(tri_price_usd))
    print(TAG + " xTRI price: ${0}".format(xtri_price_usd))

    # Calculate TWAP using historical data
    historical_price_data = get_historical_price_data()

    block = w3.eth.get_block("latest")

    # Add newest data to end of the lest
    historical_price_data.append(
        {
            "block_number": block["number"],
            "timestamp": block["timestamp"],
            "tri_price": tri_price_usd,
            "xtri_price": xtri_price_usd,
        }
    )

    # Remove items from beginning of the list that are beyond the window limit
    window_sized_historical_price_data = historical_price_data[-MAX_WINDOW_SIZE:]

    # Calculate geometric mean for all periods within the window
    tri_twap = geometric_mean(map(lambda x: x["tri_price"], window_sized_historical_price_data))
    xtri_twap = geometric_mean(map(lambda x: x["xtri_price"], window_sized_historical_price_data))

    # Upload calculated TWAPs to GCC
    twap_payload = {"TRI": tri_twap, "xTRI": xtri_twap}
    upload_to_gcc(twap_payload, TRISOLARIS_PRICES_BUCKET_FILE_PATH)

    # Trim list to maintain the max historical storage size
    max_sized_historical_price_data = historical_price_data[-MAX_HISTORICAL_WINDOW_SIZE:]

    # Upload calculated historical prices to GCC (this file is not public)
    price_history_payload = {
        "result": max_sized_historical_price_data,
        "size": len(max_sized_historical_price_data),
    }
    upload_to_gcc(price_history_payload, TRISOLARIS_TRI_XTRI_TWAP_DATA_FILE_PATH)


def get_historical_price_data():
    blob = get_google_cloud_storage_blob(
        TRISOLARIS_PRICES_BUCKET, TRISOLARIS_TRI_XTRI_TWAP_DATA_FILE_PATH
    )
    data = json.loads(blob.download_as_string(client=None))

    return data["result"]


def get_prices():
    near_price_usd = get_weighted_average_near_usd_price(w3)
    tri_price_usd = get_weighted_average_tri_usd_price(w3, near_price_usd)

    tri_xtri_ratio = getTriXTriRatio(w3)
    xtri_price_usd = tri_price_usd * tri_xtri_ratio

    return (near_price_usd, tri_price_usd, xtri_price_usd)


# Returns reserves of a pair as a tuple
# targetTokenAddress will always be index 0 of tuple
def get_target_token_pair_reserves(w3, tlpAddress, targetTokenAddress):
    pair = init_tlp(tlpAddress)
    t1 = pair.functions.token1().call()
    t0 = pair.functions.token0().call()
    reserves = pair.functions.getReserves().call()

    if t0 != targetTokenAddress and t1 != targetTokenAddress:
        raise ValueError(
            TAG + "[get_target_token_pair_reserves] Pair does not contain target token"
        )

    if t0 == targetTokenAddress:
        target_token_index = 0
        other_token_index = 1
    else:
        target_token_index = 1
        other_token_index = 0

    return (reserves[target_token_index], reserves[other_token_index])


# Gets weighted average price of wNEAR token using wNEAR/USDC and wNEAR/USDT pools
def get_weighted_average_near_usd_price(w3):
    tlpNearUsdcReserves = get_target_token_pair_reserves(w3, TLP_NEAR_USDC, WNEAR_ADDRESS)
    normalizedNearUsdcReserves = {
        "NEAR": tlpNearUsdcReserves[0] / (10**NEAR_TOKEN_DECIMALS),
        "USD": tlpNearUsdcReserves[1] / (10**6),
    }

    tlpNearUsdtReserves = get_target_token_pair_reserves(w3, TLP_NEAR_USDT, WNEAR_ADDRESS)
    normalizedNearUsdtReserves = {
        "NEAR": tlpNearUsdtReserves[0] / (10**NEAR_TOKEN_DECIMALS),
        "USD": tlpNearUsdtReserves[1] / (10**6),
    }

    totalPooledUSD = normalizedNearUsdcReserves["USD"] + normalizedNearUsdtReserves["USD"]
    tlpNearUsdcWeight = normalizedNearUsdcReserves["USD"] / totalPooledUSD
    tlpNearUsdtWeight = normalizedNearUsdtReserves["USD"] / totalPooledUSD

    tlpNearUsdtRatio = normalizedNearUsdtReserves["USD"] / normalizedNearUsdtReserves["NEAR"]
    tlpNearUsdcRatio = normalizedNearUsdcReserves["USD"] / normalizedNearUsdcReserves["NEAR"]

    return (tlpNearUsdtRatio * tlpNearUsdcWeight) + (tlpNearUsdcRatio * tlpNearUsdtWeight)


# Gets weighted average price of TRI token using TRI/wNEAR and TRI/USDT pools
def get_weighted_average_tri_usd_price(w3, near_price_usd):
    tlpTriUsdtReserves = get_target_token_pair_reserves(w3, TLP_TRI_USDT, TRI_ADDRESS)
    normalizedTriUsdtReserves = {
        "TRI": tlpTriUsdtReserves[0] / (10**TRI_TOKEN_DECIMALS),
        "USD": tlpTriUsdtReserves[1] / 10**6,
    }

    tlpTriNearReserves = get_target_token_pair_reserves(w3, TLP_TRI_NEAR, TRI_ADDRESS)
    normalizedTriNearReserves = {
        "TRI": tlpTriNearReserves[0] / (10**TRI_TOKEN_DECIMALS),
        "USD": (tlpTriNearReserves[1] / (10**NEAR_TOKEN_DECIMALS)) * near_price_usd,
    }

    totalPooledUSD = normalizedTriUsdtReserves["USD"] + normalizedTriNearReserves["USD"]
    tlpTriUsdtWeight = normalizedTriUsdtReserves["USD"] / totalPooledUSD
    tlpTriNearWeight = normalizedTriNearReserves["USD"] / totalPooledUSD

    tlpTriUsdtRatio = normalizedTriNearReserves["USD"] / normalizedTriNearReserves["TRI"]
    tlpTriNearRatio = normalizedTriUsdtReserves["USD"] / normalizedTriUsdtReserves["TRI"]

    return (tlpTriUsdtRatio * tlpTriUsdtWeight) + (tlpTriNearRatio * tlpTriNearWeight)


def upload_to_gcc(payload, file_path):
    json_data = json.dumps(payload, ensure_ascii=False, indent=4)

    blob = get_google_cloud_storage_blob(TRISOLARIS_PRICES_BUCKET, file_path)

    blob.upload_from_string(json_data, "application/json")

    # Don't serve stale data
    blob.cache_control = "no-cache"

    # Allows file to be publicly accessible
    blob.make_public()

    # Save
    blob.patch()

    print(
        TAG
        + "Uploading to gcc location: {0}/{1} complete".format(TRISOLARIS_PRICES_BUCKET, file_path)
    )


if __name__ == "__main__":
    gcc_calculate_tri_xtri_twap(None, None)
