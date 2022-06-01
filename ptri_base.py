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
    convertStablestoLP,
    updateVestingSchedule
)
from utils.node import (
    w3,
    init_usdc_maker,
    init_erc20,
    init_stablelp_maker,
    init_ptri
)
from time import time, sleep

pairs = [
    (AURORA_ADDRESS, TRI_ADDRESS),
    # (SHITZU_ADDRESS, USDC_ADDRESS),
    # (POLAR_ADDRESS, WNEAR_ADDRESS),
    # (SPOLAR_ADDRESS, WNEAR_ADDRESS),
    # (STNEAR_ADDRESS, WNEAR_ADDRESS),
    # (BSTN_ADDRESS, WNEAR_ADDRESS),
    # (ATLUNA_ADDRESS, WNEAR_ADDRESS), 
    # (ATUST_ADDRESS, WNEAR_ADDRESS),
    # (USDC_ADDRESS, WNEAR_ADDRESS),
    # (USDT_ADDRESS, WNEAR_ADDRESS),
    # (WBTC_ADDRESS, WNEAR_ADDRESS),
    # (TRI_ADDRESS, WNEAR_ADDRESS),
    # (TRI_ADDRESS, USDC_ADDRESS),
    # (TRI_ADDRESS, USDT_ADDRESS),
    # (WETH_ADDRESS, TRI_ADDRESS),
    # (WETH_ADDRESS, WNEAR_ADDRESS),
    # (WETH_ADDRESS, USDC_ADDRESS),
    # (WETH_ADDRESS, USDT_ADDRESS),
    # (AURORA_ADDRESS, WETH_ADDRESS),
    # (ASHIBAM_ADDRESS, WETH_ADDRESS),
    # (USDC_ADDRESS, USDT_ADDRESS),
    # (FLX_ADDRESS, WNEAR_ADDRESS),
    # (EMPYR_ADDRESS, USDC_ADDRESS)
    ]

TAG = "[GCC_XTRI_BASE] "

def ptri_base(timestamp):
    try:
        # 2/8/22 - Total cost of a complete run is 0.00016Ξ
        acct = getFundedAccount()
    except:
        temp_mnemonic = "test test test test test test test test test test test junk"
        acct = getAccount(temp_mnemonic)
    
    print('xtri acct balance: ' + str(w3.eth.get_balance(acct.address)/1e18) + 'Ξ')

    usdc_maker = init_usdc_maker()
    stable_lp_maker = init_stablelp_maker()
    ptri = init_ptri()
    usdc = init_erc20(USDC_ADDRESS)
    vesting_period_increment = 60
    
    usdc_amount = 0
    initial_stableLPMaker_balance = usdc.functions.balanceOf(STABLELPMAKER_ADDRESS).call()
    current_time = time()

    xtri_data = {}

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
        if initial_stableLPMaker_balance:
            pr = usdc_amount/initial_stableLPMaker_balance
        else:
            pr = usdc_amount
        apr = pr*(3600*24*365)*100/timedelta
        xtri_data["apr"] = apr    

    xtri_data["stableLPMakerUsdc"] = initial_stableLPMaker_balance
    xtri_data["convertedUsdcAmount"] = usdc_amount
    xtri_data["timestamp"] = current_time

    return xtri_data


ptri_base(1652995245)