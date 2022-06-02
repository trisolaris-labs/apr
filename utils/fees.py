import os
from eth_account import Account
from retry import retry

@retry((ValueError), delay=10, tries=5)
def convertFeesForPair(tri_maker, pair, w3, acct):
    tri_amount = 0
    try:
        transaction = {
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.getTransactionCount(acct.address),
        }
        convert_tranasction = tri_maker.functions.convert(pair[0], pair[1]).buildTransaction(transaction)
        signed = w3.eth.account.sign_transaction(convert_tranasction, acct.key)
        signed_txn = w3.eth.sendRawTransaction(signed.rawTransaction)
        txn_hash = signed_txn.hex()
        receipt = w3.eth.waitForTransactionReceipt(txn_hash, timeout=1200)
    except ValueError as e:
        if str(e).find('INSUFFICIENT_LIQUIDITY_BURNED') == -1:
            raise e
    return

@retry((ValueError), delay=10, tries=5)
def convertStablestoLP(stable_lp_maker, w3, acct):
    try:
        transaction = {
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.getTransactionCount(acct.address),
        }
        convert_tranasction = stable_lp_maker.functions.convertStables().buildTransaction(transaction)
        signed = w3.eth.account.sign_transaction(convert_tranasction, acct.key)
        signed_txn = w3.eth.sendRawTransaction(signed.rawTransaction)
        txn_hash = signed_txn.hex()
        receipt = w3.eth.waitForTransactionReceipt(txn_hash, timeout=1200)
    except ValueError as e:
        if str(e).find('INSUFFICIENT_LIQUIDITY_BURNED') == -1:
            raise e
    return


def getAccount(mnemonic):
    # Needed to use `from_mnemonic`
    Account.enable_unaudited_hdwallet_features()
    return Account.from_mnemonic(mnemonic=mnemonic)

def getFundedAccount():
    mnemonic = os.getenv("AURORA_FUNDED_MNEMONIC")
    if (mnemonic is None):
        raise ValueError('[utils::getFundedAccount] env var AURORA_FUNDED_MNEMONIC is None')

    acct = getAccount(mnemonic)

    print('[utils::getFundedAccount] Using funded account: ' + acct.address)

    return acct
