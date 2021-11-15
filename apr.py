import json
from web3 import Web3
from utils import (
    init_chef, 
    init_tlp,
    getReserveInUsdc,
    getTotalStakedInUSDC,
    getAPR,
    getTriUsdcRatio,
)

lpAddresses = {
    0: "0x63da4DB6Ef4e7C62168aB03982399F9588fCd198",
    1: "0x20F8AeFB5697B77E0BB835A8518BE70775cdA1b0",
    2: "0x03B666f3488a7992b2385B12dF7f35156d7b29cD",
    3: "0x2fe064B6c7D274082aa5d2624709bC9AE7D16C77",
    4: "0xbc8A244e8fb683ec1Fd6f88F3cc6E565082174Eb"
    }
data = []
w3 = Web3(Web3.HTTPProvider("https://mainnet.aurora.dev/"))

## chef calls
decimals = 18
chef = init_chef(w3)
totalAllocPoint = chef.functions.totalAllocPoint().call()
triPerBlock = chef.functions.triPerBlock().call()
triUsdcRatio = getTriUsdcRatio(w3)
print(triUsdcRatio)
    

for id, address in lpAddresses.items():
    print("Reached here", address)
    tlp = init_tlp(w3, address)
    poolInfo = chef.functions.poolInfo(id).call()
    assert poolInfo[0].lower() == address.lower()
    allocPoint = poolInfo[1]
    reserveInUSDC = getReserveInUsdc(w3, tlp)
    totalSupply = tlp.functions.totalSupply().call()
    totalStaked = tlp.functions.balanceOf(chef.address).call()
    totalStakedInUSDC = getTotalStakedInUSDC(totalStaked, totalSupply, reserveInUSDC)
    totalRewardRate = triPerBlock * allocPoint / (totalAllocPoint * 10**decimals) # TODO: update to return base 10 values
    totalWeeklyRewardRate = 3600*24*7*totalRewardRate # TODO: update to return base 10 values

    # USDC wNEAR
    data.append({
        "id": id,
        "lpAddress": address,
        "totalSupply": totalSupply,
        "totalStaked": totalStaked,
        "totalStakedInUSD": totalStakedInUSDC/10**6,
        "totalRewardRate": totalRewardRate,
        # "totalWeeklyRewardRate": totalWeeklyRewardRate,
        "allocPoint": allocPoint,
        "apr": getAPR(triUsdcRatio, totalRewardRate, totalStakedInUSDC)
    }) 

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)