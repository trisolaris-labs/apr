import json
from web3 import Web3
from utils import (
    CHEFV2_ADDRESS,
    init_chef,
    init_chefv2,
    init_tlp,
    getReserveInUsdc,
    getTotalStakedInUSDC,
    getAPR,
    getTriUsdcRatio,
)

v1_pools = {
    0: "0x63da4DB6Ef4e7C62168aB03982399F9588fCd198",
    1: "0x20F8AeFB5697B77E0BB835A8518BE70775cdA1b0",
    2: "0x03B666f3488a7992b2385B12dF7f35156d7b29cD",
    3: "0x2fe064B6c7D274082aa5d2624709bC9AE7D16C77",
    4: "0xbc8A244e8fb683ec1Fd6f88F3cc6E565082174Eb",
    5: "0x84b123875F0F36B966d0B6Ca14b31121bd9676AD",
    6: "0x5eeC60F348cB1D661E4A5122CF4638c7DB7A886e",
}
data = []
w3 = Web3(Web3.HTTPProvider("https://mainnet.aurora.dev/"))

## chef calls
decimals = 18
chef = init_chef(w3)
totalAllocPoint = chef.functions.totalAllocPoint().call()

triPerBlock = chef.functions.triPerBlock().call()
triUsdcRatio = getTriUsdcRatio(w3)
print(triUsdcRatio/10**12)


for id, address in v1_pools.items():
    print("V1 Reached here", address)
    tlp = init_tlp(w3, address)
    poolInfo = chef.functions.poolInfo(id).call()
    assert poolInfo[0].lower() == address.lower()
    allocPoint = poolInfo[1]
    reserveInUSDC = getReserveInUsdc(w3, tlp, triUsdcRatio)
    totalSupply = tlp.functions.totalSupply().call()
    totalStaked = tlp.functions.balanceOf(chef.address).call()
    totalStakedInUSDC = getTotalStakedInUSDC(totalStaked, totalSupply, reserveInUSDC)
    totalSecondRewardRate = (
        triPerBlock * allocPoint / (totalAllocPoint * 10 ** decimals)
    )  # TODO: update to return base 10 values
    totalWeeklyRewardRate = (
        3600 * 24 * 7 * totalSecondRewardRate
    )  # TODO: update to return base 10 values

    # Chef V1
    data.append(
        {
            "id": id,
            "poolId": id,
            "lpAddress": address,
            "totalSupply": totalSupply,
            "totalStaked": totalStaked,
            "totalStakedInUSD": totalStakedInUSDC / 10 ** 6,
            "totalRewardRate": totalWeeklyRewardRate,
            # "totalWeeklyRewardRate": totalWeeklyRewardRate,
            "allocPoint": allocPoint,
            "apr": getAPR(triUsdcRatio/10**12, totalSecondRewardRate, totalStakedInUSDC),
            "apr2": 0,
            "chefVersion": "v1",
        }
    )

#Get alloc point of dummy LP pool in Chef V1
dummyLPPoolId = 7
dummyLPToken = "0x9990a658F71248cc507Ea62946f0EB7728491B70"
dummyLpPoolInfo = chef.functions.poolInfo(dummyLPPoolId).call()
assert dummyLpPoolInfo[0].lower() == dummyLPToken.lower()
dummyLpAllocPoint = dummyLpPoolInfo[1]


# get totalSecondRewardRate for dummy LP in Chef V1
dummyLpTotalSecondRewardRate = (triPerBlock * dummyLpAllocPoint / (totalAllocPoint * 10 ** decimals))

#Chef V2 calls
chefv2 = init_chefv2(w3)
totalAllocPointV2 = chefv2.functions.totalAllocPoint().call()

v2_pools = {
    0: "0x5eeC60F348cB1D661E4A5122CF4638c7DB7A886e",
    1: "0xd1654a7713617d41A8C9530Fb9B948d00e162194",
}

for id, address in v2_pools.items():
    print("V2 Reached here", address)
    tlp = init_tlp(w3, address)
    poolInfo = chefv2.functions.poolInfo(id).call()
    allocPoint = poolInfo[2]
    reserveInUSDC = getReserveInUsdc(w3, tlp, triUsdcRatio)
    totalSupply = tlp.functions.totalSupply().call()
    totalStaked = tlp.functions.balanceOf(CHEFV2_ADDRESS).call()
    totalStakedInUSDC = getTotalStakedInUSDC(totalStaked, totalSupply, reserveInUSDC)
    totalSecondRewardRate = (
        dummyLpTotalSecondRewardRate * allocPoint / (totalAllocPointV2)
    )  # Taking TRI allocation to dummy LP in chef v1 as tri per block for chef V2
    totalWeeklyRewardRate = (
        3600 * 24 * 7 * totalSecondRewardRate
    )  # TODO: update to return base 10 values
    data.append(
            {
                "id": len(v1_pools) + id,
                "poolId": id,
                "lpAddress": address,
                "totalSupply": totalSupply,
                "totalStaked": totalStaked,
                "totalStakedInUSD": totalStakedInUSDC / 10 ** 6,
                "totalRewardRate": totalWeeklyRewardRate,
                "allocPoint": allocPoint,
                "apr": getAPR(triUsdcRatio/10**12, totalSecondRewardRate, totalStakedInUSDC),
                "apr2": 0,
                "chefVersion": "v2",
            }
    )


with open("datav2.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
