import os
import json
from web3 import Web3
from .constants import (
    CHEF_ADDRESS,
    CHEFV2_ADDRESS,
    TRIMAKER_ADDRESS,
)

web3_url = os.getenv("AURORA_W3_URL", "https://mainnet.aurora.dev/")
w3 = Web3(Web3.HTTPProvider(web3_url))

def init_contract(contract_address, json_filename):
    with open(json_filename) as json_file:
        return w3.eth.contract(
            address=contract_address,
            abi=json.load(json_file)
        )

def init_chef(w3):
    with open('abi/chef.json') as json_file:
        return w3.eth.contract(
            address=CHEF_ADDRESS,
            abi=json.load(json_file)
        )

def init_chefv2(w3):
    with open('abi/chefv2.json') as json_file:
        return w3.eth.contract(
            address=CHEFV2_ADDRESS,
            abi=json.load(json_file)
        )

def init_rewarder(w3, rewarderAddress):
    with open('abi/complexrewarder.json') as json_file:
        return w3.eth.contract(
            address=rewarderAddress,
            abi=json.load(json_file)
        )

def init_tlp(w3, lpAddress):
    with open('abi/tlp.json') as json_file:
        return w3.eth.contract(
            address=lpAddress,
            abi=json.load(json_file)
        )

def init_stable_tlp(w3, lpAddress):
    with open('abi/lpTokenUnguarded.json') as json_file:
        return w3.eth.contract(
            address=lpAddress,
            abi=json.load(json_file)
        )

def init_stable_pool(w3, address):
    with open('abi/swapFlashLoan.json') as json_file:
        return w3.eth.contract(
            address=address,
            abi=json.load(json_file)
        )


def init_tri_maker(w3):
    with open('abi/triMaker.json') as json_file:
        return w3.eth.contract(
            address=TRIMAKER_ADDRESS,
            abi=json.load(json_file)
        )

def init_erc20(w3, erc20_address):
    with open('abi/erc20.json') as json_file:
        return w3.eth.contract(
            address=erc20_address,
            abi=json.load(json_file)
        )