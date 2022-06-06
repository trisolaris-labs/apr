import json
import os
from eth_account import Account
from web3 import Web3
from utils.constants import (
    BSTN_ADDRESS,
    ATLUNA_ADDRESS,
    ATUST_ADDRESS,
    ASHIBAM_ADDRESS,
    AVAX_ADDRESS,
    BNB_ADDRESS,
    EMPYR_ADDRESS,
    FLX_ADDRESS,
    MATIC_ADDRESS,
    POLAR_ADDRESS,
    SHITZU_ADDRESS,
    SPOLAR_ADDRESS,
    STNEAR_ADDRESS,
    TRIBAR_ADDRESS,
    TRI_ADDRESS,
    WNEAR_ADDRESS,
    WETH_ADDRESS,
    AURORA_ADDRESS,
    USDC_ADDRESS,
    USDT_ADDRESS,
    WBTC_ADDRESS
)
from utils.fees import (
    convertFeesForPair,
)
from utils.node import (
    w3,
    init_usdc_maker,
    init_erc20,
)
from time import time, sleep
Account.enable_unaudited_hdwallet_features()

temp_mnemonic = "test test test test test test test test test test test junk"
acct = Account.from_mnemonic(mnemonic=temp_mnemonic)

usdc_maker = init_usdc_maker()
usdc = init_erc20(USDC_ADDRESS)

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


usdc_amount = 0
initial_stableLPMaker_balance = usdc.functions.balanceOf(STABLELPMAKER_ADDRESS).call()
current_time = time()

with open('ptri.json') as json_file:
    ptri_data = json.load(json_file)

for pair in pairs:
    usdc_amount += convertFeesForPair(usdc_maker, pair, w3, acct)
    print(usdc_amount)
    
print(current_time, initial_stableLPMaker_balance, usdc_amount)


if ptri_data["timestamp"] != 0:
    timedelta = current_time - xtri_data["timestamp"]
    # TODO: Needs to be corrected to usdc_amount/(TRI_BALANCE_IN_pTRI*PRICE_OF_TRI)
    pr = usdc_amount/initial_stableLPMaker_balance
    apr = pr*(3600*24*365)*100/timedelta
    ptri_data["apr"] = apr    

ptri_data["stableLPMakerUsdc"] = initial_stableLPMaker_balance
xtri_data["convertedUsdcAmount"] = usdc_amount
xtri_data["timestamp"] = current_time

with open('ptri.json', 'w', encoding='utf-8') as f:
    json.dump(ptri_data, f, ensure_ascii=False, indent=4)
