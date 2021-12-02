import os
from eth_account import Account
from web3 import Web3
from utils import (
    convertFeesForPair,
    init_tri_maker,
    init_erc20,
    TRIBAR_ADDRESS,
    TRI_ADDRESS,
    WNEAR_ADDRESS,
    WETH_ADDRESS,
    AURORA_ADDRESS,
    USDC_ADDRESS,
    USDT_ADDRESS,
)
from time import sleep
Account.enable_unaudited_hdwallet_features()

w3 = Web3(Web3.HTTPProvider(os.getenv("AURORA_W3_URL")))
temp_mnemonic = "test test test test test test test test test test test junk"
acct = Account.from_mnemonic(mnemonic=temp_mnemonic)

tri_maker = init_tri_maker(w3)
tri = init_erc20(w3, TRI_ADDRESS)

pairs = [
    (TRI_ADDRESS, WNEAR_ADDRESS),
    (TRI_ADDRESS, USDC_ADDRESS),
    (TRI_ADDRESS, USDT_ADDRESS),
    (AURORA_ADDRESS, TRI_ADDRESS),
    (WETH_ADDRESS, TRI_ADDRESS),
    (WETH_ADDRESS, WNEAR_ADDRESS),
    (WETH_ADDRESS, USDC_ADDRESS),
    (WETH_ADDRESS, USDT_ADDRESS),
    (AURORA_ADDRESS, WETH_ADDRESS),
    ]

tri_amount = 0
initial_triBar_balance = tri.functions.balanceOf(TRIBAR_ADDRESS).call()

for pair in pairs:
    sleep(1)
    receipt = convertFeesForPair(tri_maker, pair, w3, acct)
    for l in receipt['logs']:
        if (l['topics'][0].hex() == '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef' and l['topics'][2].hex() == "0x000000000000000000000000802119e4e253d5c19aa06a5d567c5a41596d6803"):
            tri_amount += int(l['data'], 16)
            
