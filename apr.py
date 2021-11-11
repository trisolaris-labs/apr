import json
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://mainnet.aurora.dev/"))

chefAddress = "0x474b825a605c45836Ac50398473059D4c4c6d3Db"
lpAddresses = {0: "0x20F8AeFB5697B77E0BB835A8518BE70775cdA1b0"}

with open(f'chef.json') as json_file:
    chef = w3.eth.contract(
        address=chefAddress,
        abi=json.load(json_file)
    )

totalAllocPoint = chef.functions.totalAllocPoint().call()
triPerBlock = chef.functions.triPerBlock().call()

for id, address in lpAddresses.items():
    with open(f'tlp.json') as json_file:
        tlp = w3.eth.contract(
            address=address,
            abi=json.load(json_file)
        )
    poolInfo = chef.functions.poolInfo(id).call()
    
    # USDC wNEAR
    data = {
        "id": id,
        "totalSupply": tlp.functions.totalSupply().call(),
        "totalStaked": tlp.functions.balanceOf(chefAddress).call(),
        "totalRewardRate": triPerBlock * poolInfo[1] / totalAllocPoint # TODO: update to 
    }

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
