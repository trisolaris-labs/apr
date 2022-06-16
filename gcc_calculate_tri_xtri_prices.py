"""
This file is used for Google Cloud functions to serve the weighted average price of TRI
"""

import json
import os

from web3 import Web3

from gcc_utils import get_event_id, get_google_cloud_storage_blob
from utils.constants import TRI_ADDRESS, WNEAR_ADDRESS
from utils.node import init_tlp, w3
from utils.prices import getTriXTriRatio

# Output file name
FILE_NAME = "tri_xtri_price.json"

# Google Cloud Storage
TRISOLARIS_PRICES_BUCKET = "trisolaris_public"
TRISOLARIS_PRICES_BUCKET_FILE_PATH = FILE_NAME

TAG = "[GCC_TRI_XTRI_PRICE]"

TLP_TRI_USDT = "0x61C9E05d1Cdb1b70856c7a2c53fA9c220830633c"
TLP_TRI_NEAR = "0x84b123875F0F36B966d0B6Ca14b31121bd9676AD"
TLP_NEAR_USDC = "0x20F8AeFB5697B77E0BB835A8518BE70775cdA1b0"
TLP_NEAR_USDT = "0x03B666f3488a7992b2385B12dF7f35156d7b29cD"
TRI_TOKEN_DECIMALS = 18
NEAR_TOKEN_DECIMALS = 24


# Calculates weighted average price of TRI token
# Uploads result to gcc file storage
def gcc_calculate_tri_xtri_prices(data, context):
    event_id = get_event_id(context)

    print(TAG + "Beginning Google Cloud Fn processing for event_id: {0}".format(event_id))

    nearPriceUSD = getWeightedAverageNearUSDPrice(w3)
    print(TAG + " weighted average NEAR price: ${0}".format(nearPriceUSD))

    triPriceUSD = getWeightedAverageTriUSDPrice(w3, nearPriceUSD)
    print(TAG + " weighted average TRI price: ${0}".format(triPriceUSD))

    triXtriRatio = getTriXTriRatio(w3)
    xtriPriceUSD = triPriceUSD * triXtriRatio
    print(TAG + " xTRI price: ${0}".format(xtriPriceUSD))

    prices = {"TRI": triPriceUSD, "xTRI": xtriPriceUSD}

    json_data = json.dumps(prices, ensure_ascii=False, indent=4)

    blob = get_google_cloud_storage_blob(
        TRISOLARIS_PRICES_BUCKET, TRISOLARIS_PRICES_BUCKET_FILE_PATH
    )

    blob.upload_from_string(json_data, "application/json")

    # Don't serve stale data
    blob.cache_control = "no-cache"

    # Allows file to be publicly accessible
    blob.make_public()

    # Save
    blob.patch()

    print(
        TAG
        + "Uploading to gcc location: {0}/{1} complete".format(
            TRISOLARIS_PRICES_BUCKET, TRISOLARIS_PRICES_BUCKET_FILE_PATH
        )
    )


# Returns reserves of a pair as a tuple
# targetTokenAddress will always be index 0 of tuple
def getTargetTokenPairReserves(w3, tlpAddress, targetTokenAddress):
    pair = init_tlp(tlpAddress)
    t1 = pair.functions.token1().call()
    t0 = pair.functions.token0().call()
    reserves = pair.functions.getReserves().call()

    if t0 != targetTokenAddress and t1 != targetTokenAddress:
        raise ValueError(TAG + "[getTargetTokenPairReserves] Pair does not contain target token")

    if t0 == targetTokenAddress:
        target_token_index = 0
        other_token_index = 1
    else:
        target_token_index = 1
        other_token_index = 0

    return (reserves[target_token_index], reserves[other_token_index])


# Gets weighted average price of wNEAR token using wNEAR/USDC and wNEAR/USDT pools
def getWeightedAverageNearUSDPrice(w3):
    tlpNearUsdcReserves = getTargetTokenPairReserves(w3, TLP_NEAR_USDC, WNEAR_ADDRESS)
    normalizedNearUsdcReserves = {
        "NEAR": tlpNearUsdcReserves[0] / (10**NEAR_TOKEN_DECIMALS),
        "USD": tlpNearUsdcReserves[1] / (10**6),
    }

    tlpNearUsdtReserves = getTargetTokenPairReserves(w3, TLP_NEAR_USDT, WNEAR_ADDRESS)
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
def getWeightedAverageTriUSDPrice(w3, nearPriceUSD):
    tlpTriUsdtReserves = getTargetTokenPairReserves(w3, TLP_TRI_USDT, TRI_ADDRESS)
    normalizedTriUsdtReserves = {
        "TRI": tlpTriUsdtReserves[0] / (10**TRI_TOKEN_DECIMALS),
        "USD": tlpTriUsdtReserves[1] / 10**6,
    }

    tlpTriNearReserves = getTargetTokenPairReserves(w3, TLP_TRI_NEAR, TRI_ADDRESS)
    normalizedTriNearReserves = {
        "TRI": tlpTriNearReserves[0] / (10**TRI_TOKEN_DECIMALS),
        "USD": (tlpTriNearReserves[1] / (10**NEAR_TOKEN_DECIMALS)) * nearPriceUSD,
    }

    totalPooledUSD = normalizedTriUsdtReserves["USD"] + normalizedTriNearReserves["USD"]
    tlpTriUsdtWeight = normalizedTriUsdtReserves["USD"] / totalPooledUSD
    tlpTriNearWeight = normalizedTriNearReserves["USD"] / totalPooledUSD

    tlpTriUsdtRatio = normalizedTriNearReserves["USD"] / normalizedTriNearReserves["TRI"]
    tlpTriNearRatio = normalizedTriUsdtReserves["USD"] / normalizedTriUsdtReserves["TRI"]

    return (tlpTriUsdtRatio * tlpTriUsdtWeight) + (tlpTriNearRatio * tlpTriNearWeight)


if __name__ == "__main__":
    gcc_calculate_tri_xtri_prices(None, None)
