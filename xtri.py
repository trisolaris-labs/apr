import json
from eth_account import Account
from web3 import Web3
from utils import (
    ATLUNA_ADDRESS,
    ATUST_ADDRESS,
    ASHIBAM_ADDRESS,
    AVAX_ADDRESS,
    BNB_ADDRESS,
    EMPYR_ADDRESS,
    FLX_ADDRESS,
    MATIC_ADDRESS,
    convertFeesForPair,
    getWeb3URL,
    init_tri_maker,
    init_erc20,
    TRIBAR_ADDRESS,
    TRI_ADDRESS,
    WNEAR_ADDRESS,
    WETH_ADDRESS,
    AURORA_ADDRESS,
    USDC_ADDRESS,
    USDT_ADDRESS,
    WBTC_ADDRESS
)
from time import time, sleep
Account.enable_unaudited_hdwallet_features()

web3_url = getWeb3URL()
w3 = Web3(Web3.HTTPProvider(web3_url))
temp_mnemonic = "test test test test test test test test test test test junk"
acct = Account.from_mnemonic(mnemonic=temp_mnemonic)

tri_maker = init_tri_maker(w3)
tri = init_erc20(w3, TRI_ADDRESS)

pairs = [
    (ATLUNA_ADDRESS, WNEAR_ADDRESS),
    (ATUST_ADDRESS, WNEAR_ADDRESS),
    (USDC_ADDRESS, WNEAR_ADDRESS),
    (USDT_ADDRESS, WNEAR_ADDRESS),
    (WBTC_ADDRESS, WNEAR_ADDRESS),
    (TRI_ADDRESS, WNEAR_ADDRESS),
    (TRI_ADDRESS, USDC_ADDRESS),
    (TRI_ADDRESS, USDT_ADDRESS),
    (AURORA_ADDRESS, TRI_ADDRESS),
    (WETH_ADDRESS, TRI_ADDRESS),
    (WETH_ADDRESS, WNEAR_ADDRESS),
    (WETH_ADDRESS, USDC_ADDRESS),
    (WETH_ADDRESS, USDT_ADDRESS),
    (AURORA_ADDRESS, WETH_ADDRESS),
    (ASHIBAM_ADDRESS, WETH_ADDRESS),
    (USDC_ADDRESS, USDT_ADDRESS),
    (FLX_ADDRESS, WNEAR_ADDRESS),
    (AVAX_ADDRESS, WNEAR_ADDRESS),
    (BNB_ADDRESS, WNEAR_ADDRESS),
    (MATIC_ADDRESS, WNEAR_ADDRESS),
    (EMPYR_ADDRESS, USDC_ADDRESS),
    ]


tri_amount = 0
initial_triBar_balance = tri.functions.balanceOf(TRIBAR_ADDRESS).call()
current_time = time()

with open('xtri.json') as json_file:
    xtri_data = json.load(json_file)

for pair in pairs:
    tri_amount += convertFeesForPair(tri_maker, pair, w3, acct)
    print(tri_amount)
    
print(current_time, initial_triBar_balance, tri_amount)


if xtri_data["timestamp"] != 0:
    timedelta = current_time - xtri_data["timestamp"]
    pr = tri_amount/initial_triBar_balance
    apr = pr*(3600*24*365)*100/timedelta
    xtri_data["apr"] = apr    

xtri_data["triBarTri"] = initial_triBar_balance
xtri_data["mintedTri"] = tri_amount
xtri_data["timestamp"] = current_time

with open('xtri.json', 'w', encoding='utf-8') as f:
    json.dump(xtri_data, f, ensure_ascii=False, indent=4)
