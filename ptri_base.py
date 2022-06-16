import os
from web3 import Web3
from utils.constants import TRI_ADDRESS, PTRI_ADDRESS
from utils.fees import getAccount, getFundedAccount, convertStablestoLP
from utils.node import w3, init_erc20, init_stablelp_maker
from utils.prices import getCoingeckoUSDPriceRatio
from time import time

TAG = "[PTRI_BASE] "


def ptri_base(timestamp):
    try:
        acct = getFundedAccount()
    except:
        temp_mnemonic = "test test test test test test test test test test test junk"
        acct = getAccount(temp_mnemonic)

    print(TAG + "ptri acct balance: " + str(w3.eth.get_balance(acct.address) / 1e18) + "Ξ")

    stable_lp_maker = init_stablelp_maker()
    tri = init_erc20(TRI_ADDRESS)

    tlp_amount = 0
    initial_tri_balance_in_ptri = tri.functions.balanceOf(PTRI_ADDRESS).call()
    tri_price = getCoingeckoUSDPriceRatio("trisolaris")
    current_time = time()

    ptri_data = {}

    # Stable LP Maker Operations
    tlp_amount += convertStablestoLP(stable_lp_maker, w3, acct)
    print(TAG, "tlp_amount: ", tlp_amount)
    print(TAG, current_time, initial_tri_balance_in_ptri, tlp_amount)

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

    return ptri_data


if __name__ == "__main__":
    ptri_base(None)
