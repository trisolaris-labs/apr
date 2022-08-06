from web3 import Web3
from gcc_utils import gccPrint
from utils.memoize import memoize
from utils.node import getTokenSymbol

TAG = "[TOP_POOLS_BASE]"


# Returns bool indicating if token pair exists in base pairs
def token_pair_exists_in_base_pairs_map(token0, token1, base_pairs_map):
    # If both tokens aren't in BASE_POOL_TOKEN_MAP, bail
    if token0 not in base_pairs_map or token1 not in base_pairs_map:
        return False

    # If tokens aren't complimentary, bail
    if token1 not in base_pairs_map[token0]:
        return False

    return True


@memoize
def to_checksum_address(address):
    return Web3.toChecksumAddress(address)


# Creates a map representing Covalent API pairs response:
#   {
#     [token: string]: {
#         [complimentary_token: string]: [generated fee: int]
#     }
#   }
def create_covalent_pair_fee_map(covalent_pools, fee_threshold):
    result = {}
    for pool in covalent_pools:
        fee_quote = pool["fee_24h_quote"]
        if fee_quote < fee_threshold:
            continue

        token0 = to_checksum_address(pool["token_0"]["contract_address"])
        token1 = to_checksum_address(pool["token_1"]["contract_address"])

        if token0 not in result:
            result[token0] = {}
        if token1 not in result:
            result[token1] = {}

        result[token0][token1] = fee_quote
        result[token1][token0] = fee_quote

    return result


# Filter out base pools that:
#   1) Exist in Covalent API response
#   2) Have generate fees less than FEE_THRESHOLD
def get_base_pairs_above_fee_threshold(base_pairs, covalent_pools, fee_threshold):
    covalent_pair_fee_map = create_covalent_pair_fee_map(covalent_pools, fee_threshold)

    result = []
    for pair in base_pairs:
        [token0, token1] = pair
        fee = covalent_pair_fee_map.get(token0, {}).get(token1)

        # If fee is less than threshold, filter it out
        if fee is not None and fee < fee_threshold:
            gccPrint(
                f"{TAG} Skipping base pair {getTokenSymbol(token0)}:{getTokenSymbol(token1)}: Fee is below ${fee_threshold} threshold"
            )
        else:
            result.append(pair)

    return result


# Map of addres => address[] pairs
def create_base_pools_map(base_pairs):
    result = {}
    for pair in base_pairs:
        token0, token1 = pair

        # Initialize values to empty list
        if token0 not in result:
            result[token0] = []
        if token1 not in result:
            result[token1] = []

        # Append complimentary token
        result[token0].append(token1)
        result[token1].append(token0)

    return result
