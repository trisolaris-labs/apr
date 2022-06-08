from datetime import datetime
import os
from requests import ReadTimeout
from web3 import Web3
import math
from utils.constants import (
    ATLUNA_ADDRESS,
    ATUST_ADDRESS,
    ASHIBAM_ADDRESS,
    TRI_ADDRESS,
    WNEAR_ADDRESS,
    WETH_ADDRESS,
    AURORA_ADDRESS,
    USDC_ADDRESS,
    USDT_ADDRESS,
    WBTC_ADDRESS,
    SHITZU_ADDRESS,
    POLAR_ADDRESS,
    SPOLAR_ADDRESS,
    STNEAR_ADDRESS,
    BSTN_ADDRESS,
    FLX_ADDRESS,
    EMPYR_ADDRESS
)
from utils.fees import (
    convertFeesForPair,
    getAccount,
    getFundedAccount
)
from utils.node import (
    w3,
    init_usdc_maker
)
from time import time, sleep

pairs = [
    (AURORA_ADDRESS, TRI_ADDRESS),
    (SHITZU_ADDRESS, USDC_ADDRESS),
    (POLAR_ADDRESS, WNEAR_ADDRESS),
    (SPOLAR_ADDRESS, WNEAR_ADDRESS),
    (STNEAR_ADDRESS, WNEAR_ADDRESS),
    (BSTN_ADDRESS, WNEAR_ADDRESS),
    (ATLUNA_ADDRESS, WNEAR_ADDRESS), 
    (ATUST_ADDRESS, WNEAR_ADDRESS),
    (USDC_ADDRESS, WNEAR_ADDRESS),
    (USDT_ADDRESS, WNEAR_ADDRESS),
    (WBTC_ADDRESS, WNEAR_ADDRESS),
    (TRI_ADDRESS, WNEAR_ADDRESS),
    (TRI_ADDRESS, USDC_ADDRESS),
    (TRI_ADDRESS, USDT_ADDRESS),
    (WETH_ADDRESS, TRI_ADDRESS),
    (WETH_ADDRESS, WNEAR_ADDRESS),
    (WETH_ADDRESS, USDC_ADDRESS),
    (WETH_ADDRESS, USDT_ADDRESS),
    (AURORA_ADDRESS, WETH_ADDRESS),
    (ASHIBAM_ADDRESS, WETH_ADDRESS),
    (USDC_ADDRESS, USDT_ADDRESS),
    (FLX_ADDRESS, WNEAR_ADDRESS),
    (EMPYR_ADDRESS, USDC_ADDRESS)
    ]

TAG = "[PTRI_FEES_BASE] "

def ptri_fees_base(frequency = 24):
    try:
        acct = getFundedAccount()
    except:
        temp_mnemonic = "test test test test test test test test test test test junk"
        acct = getAccount(temp_mnemonic)
    
    print(TAG + 'ptri acct balance: ' + str(w3.eth.get_balance(acct.address)/1e18) + 'Ξ')

    usdc_maker = init_usdc_maker()
    current_time = time()

    #USDC Maker Operations
    start_index, limit = getRange(frequency)
    chunks = [pairs[x] for x in range(start_index, limit)]
    for pair in chunks:
        print(TAG, current_time, "STARTING", pair)
        sleep(5)
        try:
            tx = convertFeesForPair(usdc_maker, pair, w3, acct)
            print(TAG, current_time, "SUCCESS", pair, tx)
        except ReadTimeout as e:
            print(TAG, current_time, "ERROR", pair, e)

# Based on the frequency this method is called
# Gives an index range based on 
#   (1) current hour
#   (2) length of items in `pairs`
def getRange(frequency = 24):
  pairs_length = len(pairs)
  current_hour = datetime.now().hour
  start_index = (((current_hour / 24) * frequency) / frequency) * pairs_length
  start_index = math.floor(start_index)
  step = pairs_length / frequency
  limit = min(math.ceil(start_index + step), pairs_length)

  return start_index, limit
    
def normalize(values, actual_bounds, desired_bounds):
    return [desired_bounds[0] + (x - actual_bounds[0]) * (desired_bounds[1] - desired_bounds[0]) / (actual_bounds[1] - actual_bounds[0]) for x in values]

if __name__ == "__main__":
    ptri_fees_base(None)