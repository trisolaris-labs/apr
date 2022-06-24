from web3 import Web3
from gcc_utils import gccPrint
from utils import covalent

TAG = "[TOP_POOLS_BASE] "

def top_pools_base():
    gccPrint(TAG + "Starting")

    pools = covalent.getPools()

    top_pool_tokens = []
    for pool in pools:
        if pool['fee_24h_quote'] >= 1:
            token0 = Web3.toChecksumAddress(pool['token_0']['contract_address'])
            token1 = Web3.toChecksumAddress(pool['token_1']['contract_address'])
            top_pool_tokens.append([token0, token1])

    return top_pool_tokens


if __name__ == "__main__":
    top_pools_base()
