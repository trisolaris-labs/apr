"""
This file is used for Google Cloud functions to serve circulating supply calculations
"""

import os

from web3 import Web3
from utils import (init_erc20, TRI_ADDRESS)
from gcc_utils import (get_event_id, upload_object_as_text_to_gcc)

# Output file name
FILE_NAME = "circulating_supply.txt"

# Google Cloud Storage
TRISOLARIS_APR_BUCKET = "trisolaris_public"
TRISOLARIS_APR_BUCKET_FILE_PATH = FILE_NAME

# This is the tx where 160MM TRI was locked
LOCKED_TRI_TRANSACTION_HASH = '0x93026b0e7150837de8180890d4f1790bf14f3bc36f771433717830647c1a0516'

TAG = "[GCC TOTAL CIRC]"

web3_url = os.getenv("AURORA_W3_URL", "https://mainnet.aurora.dev/")
w3 = Web3(Web3.HTTPProvider(web3_url))
tri = init_erc20(w3, TRI_ADDRESS)

# Calculated total circulating supply of TRI
# Uploads result to gcc file storage
def gcc_total_circulating_supply(data, context):
    event_id = get_event_id(context)

    print(TAG + "Beginning Google Cloud Fn processing for event_id: {0}".format(event_id))
    
    current_total_supply = tri.functions.totalSupply().call()
    decimals = tri.functions.decimals().call()

    locked_tri = get_locked_tri()

    circulating_supply = current_total_supply - locked_tri

    circulating_supply_formatted = str(circulating_supply / (10 ** decimals))

    print(TAG + " TRI: {0}".format(circulating_supply_formatted))

    upload_object_as_text_to_gcc(
        circulating_supply_formatted,
        gcc_bucket=TRISOLARIS_APR_BUCKET,
        gcc_file_path=TRISOLARIS_APR_BUCKET_FILE_PATH,
        make_public=True,
    )

def get_locked_tri():
    transaction_receipt = w3.eth.get_transaction_receipt(LOCKED_TRI_TRANSACTION_HASH)
    data = transaction_receipt.logs[0].data
    locked_tri = int(data, 16)

    return locked_tri


if __name__ == "__main__":
    gcc_total_circulating_supply(None, None)