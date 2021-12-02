from eth_account import Account
from web3 import Web3
from utils import (
    init_tri_maker,
    init_erc20,
    TRIBAR_ADDRESS,
    TRI_ADDRESS,
    WNEAR_ADDRESS,
    WETH_ADDRESS,
)
from time import sleep
Account.enable_unaudited_hdwallet_features()

w3 = Web3(Web3.HTTPProvider("https://mainnet.aurora.dev"))
temp_mnemonic = "test test test test test test test test test test test junk"
acct = Account.from_mnemonic(mnemonic=temp_mnemonic)

tri_maker = init_tri_maker(w3)
tri = init_erc20(w3, TRI_ADDRESS)
transaction = {
    'gasPrice': w3.eth.gas_price,
    'nonce': w3.eth.getTransactionCount(acct.address)
}

pre_triBar_balance = tri.functions.balanceOf(TRIBAR_ADDRESS).call()
convert_tranasction = tri_maker.functions.convert(
    WNEAR_ADDRESS, WETH_ADDRESS
).buildTransaction(transaction)
signed = w3.eth.account.sign_transaction(convert_tranasction, acct.key)
signed_txn = w3.eth.sendRawTransaction(signed.rawTransaction)
txn_hash = signed_txn.hex()
receipt = w3.eth.waitForTransactionReceipt(txn_hash, timeout=1200)

sleep(1)
post_triBar_balance = tri.functions.balanceOf(TRIBAR_ADDRESS).call()

print(pre_triBar_balance, post_triBar_balance)
