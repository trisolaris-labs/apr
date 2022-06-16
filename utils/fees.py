import os

from eth_account import Account
from retry import retry


@retry((ValueError), delay=10, tries=5)
def convertFeesForPair(tri_maker, pair, w3, acct):
    usdc_amount = 0
    try:
        transaction = {
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.getTransactionCount(acct.address),
        }
        convert_tranasction = tri_maker.functions.convert(
            pair[0], pair[1]
        ).buildTransaction(transaction)
        signed = w3.eth.account.sign_transaction(convert_tranasction, acct.key)
        signed_txn = w3.eth.sendRawTransaction(signed.rawTransaction)
        txn_hash = signed_txn.hex()
        receipt = w3.eth.waitForTransactionReceipt(txn_hash, timeout=1200)
        for log in receipt["logs"]:
            if (
                log["topics"][0].hex()
                == "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
                and log["topics"][2].hex()
                == "0x000000000000000000000000802119e4e253d5c19aa06a5d567c5a41596d6803"
            ):
                usdc_amount += int(log["data"], 16)
    except ValueError as e:
        if str(e).find("INSUFFICIENT_LIQUIDITY_BURNED") == -1:
            raise e
    return usdc_amount


@retry((ValueError), delay=10, tries=5)
def convertFeesForPairs(tri_maker, pairs, w3, acct):
    token0 = []
    token1 = []
    for pair in pairs:
        token0.append(pair[0])
        token1.append(pair[1])
    try:
        transaction = {
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.getTransactionCount(acct.address),
        }
        convert_tranasction = tri_maker.functions.convertMultiple(
            token0, token1
        ).buildTransaction(transaction)
        signed = w3.eth.account.sign_transaction(convert_tranasction, acct.key)
        signed_txn = w3.eth.sendRawTransaction(signed.rawTransaction)
        txn_hash = signed_txn.hex()
        w3.eth.waitForTransactionReceipt(txn_hash, timeout=1200)
    except ValueError as e:
        if str(e).find("INSUFFICIENT_LIQUIDITY_BURNED") == -1:
            raise e


@retry((ValueError), delay=10, tries=5)
def convertStablestoLP(stable_lp_maker, w3, acct):
    tlp_amount = 0
    try:
        transaction = {
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.getTransactionCount(acct.address),
        }
        convert_tranasction = (
            stable_lp_maker.functions.convertStables().buildTransaction(transaction)
        )
        signed = w3.eth.account.sign_transaction(convert_tranasction, acct.key)
        signed_txn = w3.eth.sendRawTransaction(signed.rawTransaction)
        txn_hash = signed_txn.hex()
        receipt = w3.eth.waitForTransactionReceipt(txn_hash, timeout=1200)
        for log in receipt["logs"]:
            # checks for LogLpTokensSentTopTRI event
            if (
                log["topics"][0].hex()
                == "0x0449e4bb1174156d2eca3c858613207c8abf4f2ec58f11e5bf7e148331428180"
            ):
                tlp_amount += int(log["data"], 16)
    except ValueError as e:
        if str(e).find("INSUFFICIENT_LIQUIDITY_BURNED") == -1:
            raise e
    return tlp_amount


def getAccount(mnemonic):
    # Needed to use `from_mnemonic`
    Account.enable_unaudited_hdwallet_features()
    return Account.from_mnemonic(mnemonic=mnemonic)


def getFundedAccount():
    mnemonic = os.getenv("AURORA_FUNDED_MNEMONIC")
    if mnemonic is None:
        raise ValueError(
            "[utils::getFundedAccount] env var AURORA_FUNDED_MNEMONIC is None"
        )

    acct = getAccount(mnemonic)

    print("[utils::getFundedAccount] Using funded account: " + acct.address)

    return acct
