from datetime import datetime
import time
from requests import ReadTimeout
import requests
import math
from gcc_utils import gccPrint
from utils.fees import (
    convertFeesForPair,
    getAccount,
    getFundedAccount
)
from utils.node import (
    getTokenSymbol,
    w3,
    init_usdc_maker
)

TAG = "[PTRI_FEES_BASE] "
TOP_PAIRS_ENDPOINT = "https://cdn.trisolaris.io/pools.json"

def ptri_fees_base(frequency = 24):
    try:
        acct = getFundedAccount()
    except:
        temp_mnemonic = "test test test test test test test test test test test junk"
        acct = getAccount(temp_mnemonic)
    
    gccPrint(TAG + 'ptri acct balance: ' + str(w3.eth.get_balance(acct.address)/1e18) + 'Ξ')

    usdc_maker = init_usdc_maker()

    #USDC Maker Operations
    pairs = requests.get(TOP_PAIRS_ENDPOINT).json()
    start_index, limit = getRange(len(pairs), frequency)
    chunks = [pairs[x] for x in range(start_index, limit)]
    for pair in chunks:
        pairSymbols = ":".join(map(lambda x: getTokenSymbol(x), pair))
        try:
            convertFeesForPair(usdc_maker, pair, w3, acct)
            gccPrint(f"{TAG}{pairSymbols} {getTime()} SUCCESS")
        except ReadTimeout as e:
            gccPrint(f"{TAG}{pairSymbols} {getTime()} {e}", "ERROR")
        finally:
            time.sleep(5)

# Based on the frequency this method is called
# Gives an index range based on 
#   (1) current hour
#   (2) length of items in `pairs`
def getRange(quantity, frequency = 24):
  current_hour = datetime.now().hour
  start_index = (((current_hour / 24) * frequency) / frequency) * quantity
  start_index = math.floor(start_index)
  step = quantity / frequency
  limit = min(math.ceil(start_index + step), quantity)

  return start_index, limit
    
def normalize(values, actual_bounds, desired_bounds):
    return [desired_bounds[0] + (x - actual_bounds[0]) * (desired_bounds[1] - desired_bounds[0]) / (actual_bounds[1] - actual_bounds[0]) for x in values]

def getTime():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time

if __name__ == "__main__":
    ptri_fees_base(None)