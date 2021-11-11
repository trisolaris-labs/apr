import json
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://mainnet.aurora.dev/"))

chefAddress = "0x474b825a605c45836Ac50398473059D4c4c6d3Db"
lpAddress = "0x20F8AeFB5697B77E0BB835A8518BE70775cdA1b0"

with open(f'chef.json') as json_file:
    chef = w3.eth.contract(
        address=chefAddress,
        abi=json.load(json_file)
    )

with open(f'tlp.json') as json_file:
    tlp = w3.eth.contract(
        address=lpAddress,
        abi=json.load(json_file)
    )

# USDC wNEAR
data = {
    "id": 0,
    "totalSupply": tlp.functions.totalSupply().call(),
    "totalStaked": tlp.functions.balanceOf(chefAddress).call(),
}

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
