"""
This file is used for Google Cloud functions to serve circulating supply calculations
"""

import os
import json

from web3 import Web3
from utils.node import init_erc20
from utils.constants import TRI_ADDRESS
from gcc_utils import get_event_id, get_google_cloud_storage_blob

# Output file name
FILE_NAME = "circulating_supply.json"

FILES = [
    {"content_type": "application/json", "path": "circulating_supply.json"},
    {"content_type": "text/plain", "path": "circulating_supply.txt"},
]

# Google Cloud Storage
TRISOLARIS_APR_BUCKET = "trisolaris_public"
TRISOLARIS_APR_BUCKET_FILE_PATH = FILE_NAME

# This is the tx where 160MM TRI was locked
LOCKED_TRI_TRANSACTION_HASH = (
    "0x93026b0e7150837de8180890d4f1790bf14f3bc36f771433717830647c1a0516"
)

TAG = "[GCC TOTAL CIRC]"

web3_url = os.getenv("AURORA_W3_URL", "https://mainnet.aurora.dev/")
w3 = Web3(Web3.HTTPProvider(web3_url))
tri = init_erc20(TRI_ADDRESS)

# Calculated total circulating supply of TRI
# Uploads result to gcc file storage
def gcc_total_circulating_supply(data, context):
    event_id = get_event_id(context)

    print(
        TAG + "Beginning Google Cloud Fn processing for event_id: {0}".format(event_id)
    )

    circulating_supply = str(get_total_circulating_supply())

    print(TAG + " TRI: {0}".format(circulating_supply))

    for file in FILES:
        upload_to_gcs(
            TRISOLARIS_APR_BUCKET,
            file["path"],
            file["content_type"],
            circulating_supply,
        )


def upload_to_gcs(bucket, path, content_type, data):
    blob = get_google_cloud_storage_blob(bucket, path)

    blob.upload_from_string(data, content_type)

    # Don't serve stale data
    blob.cache_control = "no-cache"

    # Allows file to be publicly accessible
    blob.make_public()

    # Save
    blob.patch()

    print(TAG + " Uploading to gcc location: {0}/{1} complete".format(bucket, path))


def get_locked_tri():
    transaction_receipt = w3.eth.get_transaction_receipt(LOCKED_TRI_TRANSACTION_HASH)
    data = transaction_receipt.logs[0].data
    locked_tri = int(data, 16)

    return locked_tri


def get_total_circulating_supply():
    current_total_supply = tri.functions.totalSupply().call()
    decimals = tri.functions.decimals().call()

    locked_tri = get_locked_tri()

    circulating_supply = current_total_supply - locked_tri

    return circulating_supply / (10**decimals)


if __name__ == "__main__":
    gcc_total_circulating_supply(None, None)
