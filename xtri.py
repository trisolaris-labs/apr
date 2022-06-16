import json
from time import time

from eth_account import Account

from utils.constants import (
    ASHIBAM_ADDRESS,
    ATLUNA_ADDRESS,
    ATUST_ADDRESS,
    AURORA_ADDRESS,
    AVAX_ADDRESS,
    BNB_ADDRESS,
    BSTN_ADDRESS,
    EMPYR_ADDRESS,
    FLX_ADDRESS,
    MATIC_ADDRESS,
    POLAR_ADDRESS,
    SHITZU_ADDRESS,
    SPOLAR_ADDRESS,
    STNEAR_ADDRESS,
    TRI_ADDRESS,
    TRIBAR_ADDRESS,
    USDC_ADDRESS,
    USDT_ADDRESS,
    WBTC_ADDRESS,
    WETH_ADDRESS,
    WNEAR_ADDRESS,
)
from utils.fees import convertFeesForPair
from utils.node import init_erc20, init_tri_maker, w3

Account.enable_unaudited_hdwallet_features()

temp_mnemonic = "test test test test test test test test test test test junk"
acct = Account.from_mnemonic(mnemonic=temp_mnemonic)

tri_maker = init_tri_maker()
tri = init_erc20(TRI_ADDRESS)

pairs = [
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

with open("xtri.json") as json_file:
    xtri_data = json.load(json_file)

for pair in pairs:
    tri_amount += convertFeesForPair(tri_maker, pair, w3, acct)
    print(tri_amount)

print(current_time, initial_triBar_balance, tri_amount)


if xtri_data["timestamp"] != 0:
    timedelta = current_time - xtri_data["timestamp"]
    pr = tri_amount / initial_triBar_balance
    apr = pr * (3600 * 24 * 365) * 100 / timedelta
    xtri_data["apr"] = apr

xtri_data["triBarTri"] = initial_triBar_balance
xtri_data["mintedTri"] = tri_amount
xtri_data["timestamp"] = current_time

with open("xtri.json", "w", encoding="utf-8") as f:
    json.dump(xtri_data, f, ensure_ascii=False, indent=4)
