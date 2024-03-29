import os
import json
from web3 import Web3

from .memoize import memoize
from .constants import (
    FACTORY_ADDRESS,
    CHEF_ADDRESS,
    CHEFV2_ADDRESS,
    PTRI_ADDRESS,
    TRIMAKER_ADDRESS,
    STABLELPMAKERV4_ADDRESS,
    STABLELPMAKERV3_ADDRESS,
    USDCMAKER_ADDRESS,
    STABLELPMAKERV2_ADDRESS,
)

web3_url = os.getenv("AURORA_W3_URL", "https://mainnet.aurora.dev/")
w3 = Web3(Web3.HTTPProvider(web3_url))


def init_contract(contract_address, json_filename):
    with open(json_filename) as json_file:
        return w3.eth.contract(address=contract_address, abi=json.load(json_file))


def init_chef():
    return init_contract(CHEF_ADDRESS, "abi/chef.json")


def init_chefv2():
    return init_contract(CHEFV2_ADDRESS, "abi/chefv2.json")


def init_rewarder(rewarderAddress):
    return init_contract(rewarderAddress, "abi/complexrewarder.json")


def init_n_rewarder(rewarderAddress):
    return init_contract(rewarderAddress, "abi/complex_n_rewarder.json")


def init_tlp(lpAddress):
    return init_contract(lpAddress, "abi/tlp.json")


def init_stable_tlp(lpAddress):
    return init_contract(lpAddress, "abi/lpTokenUnguarded.json")


def init_stable_pool(address):
    return init_contract(address, "abi/swapFlashLoan.json")


def init_tri_maker():
    return init_contract(TRIMAKER_ADDRESS, "abi/triMaker.json")


def init_usdc_maker():
    return init_contract(USDCMAKER_ADDRESS, "abi/usdcMaker.json")


def init_stablelp_maker_v2():
    return init_contract(STABLELPMAKERV2_ADDRESS, "abi/stableLpMakerV2.json")


def init_stablelp_maker_v3():
    return init_contract(STABLELPMAKERV3_ADDRESS, "abi/stableLpMakerV3.json")


def init_stablelp_maker_v4():
    return init_contract(STABLELPMAKERV4_ADDRESS, "abi/stableLpMakerV3.json")


def init_ptri():
    return init_contract(PTRI_ADDRESS, "abi/pTri.json")


def init_erc20(erc20_address):
    return init_contract(erc20_address, "abi/erc20.json")


def init_aurigami_erc20(au_erc20_address):
    return init_contract(au_erc20_address, "abi/au_erc20.json")

def init_uniswap_v2_factory():
    return init_contract(FACTORY_ADDRESS, "abi/IuniswapV2Factory.json")

@memoize
def getTokenSymbol(address):
    token = init_erc20(address)
    return token.functions.symbol().call()
