import json
from utils import (
    TRI_ADDRESS,
    init_chef, 
    init_tlp,
    WETH_ADDRESS,
    WNEAR_ADDRESS,
    DAI_ADDRESS,
    USDC_ADDRESS,
    FACTORY_ADDRESS
)
from web3 import Web3

lpAddresses = {0: "0x20F8AeFB5697B77E0BB835A8518BE70775cdA1b0"}
data = []
w3 = Web3(Web3.HTTPProvider("https://mainnet.aurora.dev/"))

## chef calls
chef = init_chef(w3)
totalAllocPoint = chef.functions.totalAllocPoint().call()
triPerBlock = chef.functions.triPerBlock().call()

for id, address in lpAddresses.items():
    tlp = init_tlp(w3, address)
    poolInfo = chef.functions.poolInfo(id).call()
    
    # USDC wNEAR
    data.append({
        "id": id,
        "totalSupply": tlp.functions.totalSupply().call(),
        "totalStaked": tlp.functions.balanceOf(chef.address).call(),
        "totalRewardRate": triPerBlock * poolInfo[1] / totalAllocPoint # TODO: update to return base 10 values
    }) 

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)