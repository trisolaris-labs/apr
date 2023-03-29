import os
from web3 import Web3
from utils.constants import TRI_ADDRESS, PTRI_ADDRESS
from utils.fees import getAccount, getFundedAccount, convertStablestoLP
from utils.node import init_stablelp_maker_v4, w3, init_erc20
from utils.prices import getCoingeckoUSDPriceRatio
from gcc_utils import gccPrint
from time import time

TAG = "[PTRI_BASE] "


def ptri_base(timestamp):
    try:
        acct = getFundedAccount()
    except:
        temp_mnemonic = "test test test test test test test test test test test junk"
        acct = getAccount(temp_mnemonic)

    gccPrint(
        TAG + "ptri acct balance: " + str(w3.eth.get_balance(acct.address) / 1e18) + "Ξ"
    )

    stable_lp_maker = init_stablelp_maker_v4()
    tri = init_erc20(TRI_ADDRESS)

    tlp_amount = 0
    initial_tri_balance_in_ptri = tri.functions.balanceOf(PTRI_ADDRESS).call()
    tri_price = getCoingeckoUSDPriceRatio("trisolaris")
    current_time = time()

    ptri_data = {}

    # Stable LP Maker Operations
    tlp_amount += convertStablestoLP(stable_lp_maker, w3, acct)
    gccPrint(f"{TAG} tlp_amount: {tlp_amount/1e18}")
    gccPrint(f"{TAG} initial tri balance: {initial_tri_balance_in_ptri/1e18}")

    if timestamp != 0 and timestamp != None:
        timedelta = current_time - timestamp
        if initial_tri_balance_in_ptri:
            pr = (tlp_amount * tri_price) / (initial_tri_balance_in_ptri)
        else:
            pr = tlp_amount * tri_price
        apr = pr * (3600 * 24 * 365) * 100 / timedelta
        ptri_data["apr"] = apr

    ptri_data["triBalance"] = initial_tri_balance_in_ptri
    ptri_data["convertedUsdcAmount"] = tlp_amount
    ptri_data["tri_price"] = tri_price
    ptri_data["timestamp"] = current_time

    gccPrint(
        f"{TAG} apr: {apr}, triBalance: {initial_tri_balance_in_ptri}, convertedUsdcAmount: {tlp_amount}, tri_price: {tri_price}, timestamp: {current_time}"
    )

    return ptri_data


if __name__ == "__main__":
    ptri_base(1678219208)


############################################################
####### BEFORE RUNNING THIS, SEE `ptri_fees_base.py` #######
############################################################
"""
Since there's a delay, we need to update the following on ptri.json:
0. BEFORE RUNNING THIS, SEE `ptri_fees_base.py`

1. Update line 63 to with the last timestamp from `https://cdn.trisolaris.io/ptri.json`
2. Run this script and save the terminal output
3. Create compatible JSON object from lines 53-57
4. Download JSON object here: https://cdn.trisolaris.io/ptri.json
5. Save JSON object here AGAIN: https://cdn.trisolaris.io/ptri.json, except as `ptri_backup.json`
6. Open `ptri.json`, and add object from 1. to the downloaded file.
7. Upload (drag and drop) your new `ptri.json` (with the additional JSON object) to https://console.cloud.google.com/storage/browser/trisolaris_public;tab=objects?forceOnBucketsSortingFiltering=false&project=trisolaris-ad-hoc&prefix=&forceOnObjectsSortingFiltering=false
  - When "Resolve object conflict" modal shows, click "Overwrite object"
8. Load up trisolaris.io/stake and confirm data.  It can take 10-30 seconds to update.z
  - If it doesn't look right, do 5. but rename `ptri_backup.json` to `ptri.json`, and upload that to undo the changes.
"""