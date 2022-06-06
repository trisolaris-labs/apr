import os
from web3 import Web3
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
    EMPYR_ADDRESS,
    STABLELPMAKER_ADDRESS
)
from utils.fees import (
    convertFeesForPair,
    getAccount,
    getFundedAccount,
    convertStablestoLP
)
from utils.node import (
    w3,
    init_usdc_maker,
    init_erc20,
    init_stablelp_maker
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

TAG = "[GCC_PTRI_BASE] "

def ptri_base(timestamp):
    try:
        acct = getFundedAccount()
    except:
        temp_mnemonic = "test test test test test test test test test test test junk"
        acct = getAccount(temp_mnemonic)
    
    print(TAG + 'ptri acct balance: ' + str(w3.eth.get_balance(acct.address)/1e18) + 'Ξ')

    usdc_maker = init_usdc_maker()
    stable_lp_maker = init_stablelp_maker()
    usdc = init_erc20(USDC_ADDRESS)
    
    usdc_amount = 0
    initial_stableLPMaker_balance = usdc.functions.balanceOf(STABLELPMAKER_ADDRESS).call()
    current_time = time()

    ptri_data = {}

    #USDC Maker Operations
    for pair in pairs:
        sleep(5)
        usdc_amount += convertFeesForPair(usdc_maker, pair, w3, acct)
        print(TAG, 'usdc_amount: ',  usdc_amount)
        
    print(TAG, current_time, initial_stableLPMaker_balance, usdc_amount)

    #Stable LP Maker Operations
    convertStablestoLP(stable_lp_maker, w3, acct)

    if timestamp != 0 and timestamp != None:
        timedelta = current_time - timestamp
        # TODO: Change to usdc_amount/(TRI_BALANCE_IN_pTRI*PRICE_OF_TRI)
        if initial_stableLPMaker_balance:
            pr = usdc_amount/initial_stableLPMaker_balance
        else:
            pr = usdc_amount
        apr = pr*(3600*24*365)*100/timedelta
        ptri_data["apr"] = apr    

    ptri_data["stableLPMakerUsdc"] = initial_stableLPMaker_balance
    ptri_data["convertedUsdcAmount"] = usdc_amount
    ptri_data["timestamp"] = current_time

    return ptri_data

if __name__ == "__main__":
    ptri_base(None)