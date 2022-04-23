from .node import (
    init_erc20, 
    init_stable_pool, 
    init_tlp,
    init_rewarder
)
from .constants import (
    USDC_ADDRESS, 
    USDT_ADDRESS,
    WNEAR_ADDRESS,
    WETH_ADDRESS,
    TRI_ADDRESS,
    TRIBAR_ADDRESS,
    XNL_ADDRESS,
    ZERO_ADDRESS,
    V1_POOLS,
    V2_STABLEPOOL_FACTORY,
)
from .prices import (
    getTriXTriRatio,
    getTokenUSDRatio,
)

# have function that gets balance of underlying tokens, and then multiply 1
# add value and then get reserve
# LP token address does not hold tokens, other address does so need both
def getReserveStables(w3, total_supply, address):
    stable_pool_contract = init_stable_pool(address)
    virtual_price = stable_pool_contract.functions.getVirtualPrice().call()
    reserve = (virtual_price * total_supply)/(10**36)
    return reserve

def getReserveInUsd(w3, tlp, triUsdRatio, wnearUsdRatio, wethUsdRatio):
    t0 = tlp.functions.token0().call()
    t1 = tlp.functions.token1().call()
    reserves = tlp.functions.getReserves().call()
    if (t0 == USDC_ADDRESS or t1 == USDC_ADDRESS):
        decimals = init_erc20(USDC_ADDRESS).functions.decimals().call()
        if t0 == USDC_ADDRESS:
            return reserves[0]*2/10**decimals
        else:
            return reserves[1]*2/10**decimals
    elif (t0 == WNEAR_ADDRESS or t1 == WNEAR_ADDRESS):
        decimals = init_erc20(WNEAR_ADDRESS).functions.decimals().call()
        if t0 == WNEAR_ADDRESS:
            reserveInWnear = reserves[0]*2/10**decimals
        else:
            reserveInWnear = reserves[1]*2/10**decimals
        return reserveInWnear/wnearUsdRatio
    elif (t0 == WETH_ADDRESS or t1 == WETH_ADDRESS):
        decimals = init_erc20(WETH_ADDRESS).functions.decimals().call()
        if t0 == WETH_ADDRESS:
            reserveInWeth = reserves[0]*2/10**decimals
        else:
            reserveInWeth = reserves[1]*2/10**decimals
        return reserveInWeth/wethUsdRatio
    elif (t0 == TRI_ADDRESS or t1 == TRI_ADDRESS ):
        decimals = init_erc20(TRI_ADDRESS).functions.decimals().call()
        if t0 == TRI_ADDRESS:
            reserveInTri = reserves[0]*2/10**decimals
        else:
            reserveInTri = reserves[1]*2/10**decimals
        return reserveInTri/triUsdRatio
    elif (t0 == TRIBAR_ADDRESS or t1 == TRIBAR_ADDRESS ):
        decimals = init_erc20(TRIBAR_ADDRESS).functions.decimals().call()
        if t0 == TRIBAR_ADDRESS:
            reserveInXTri = reserves[0]*2/10**decimals
        else:
            reserveInXTri = reserves[1]*2/10**decimals
        return reserveInXTri*getTriXTriRatio(w3)/triUsdRatio
    elif (t0 == XNL_ADDRESS or t1 == XNL_ADDRESS ):
        decimals = init_erc20(XNL_ADDRESS).functions.decimals().call()
        if t0 == XNL_ADDRESS:
            reserveInTri = reserves[0]*2/10**decimals
        else:
            reserveInTri = reserves[1]*2/10**decimals
        return reserveInTri/triUsdRatio
    elif (t0 == USDT_ADDRESS or t1 == USDT_ADDRESS):
        decimals = init_erc20(USDT_ADDRESS).functions.decimals().call()
        if t0 == USDT_ADDRESS:
            return reserves[0]*2/10**decimals
        else:
            return reserves[1]*2/10**decimals
    

def getTotalStakedInUSD(totalStaked, totalAvailable, reserveInUSD):
    if totalAvailable == 0:
        return 0
    else:
        return totalStaked*reserveInUSD/totalAvailable


def getAPR(tokenUsdRatio, totalRewardRate, totalStakedInUSD):
    if (totalStakedInUSD == 0 or tokenUsdRatio == 0):
        return 0
    else:
        totalYearlyRewards = totalRewardRate * 3600 * 24 * 365
        return totalYearlyRewards*100/(totalStakedInUSD*tokenUsdRatio)


def getDataV1Pools(w3, id, address, chef, triPerBlock, totalAllocPoint, tri_decimals, triUsdRatio, wnearUsdRatio, wethUsdRatio):
    tlp = init_tlp(address)
    poolInfo = chef.functions.poolInfo(id).call()
    assert poolInfo[0].lower() == address.lower()
    allocPoint = poolInfo[1]
    reserveInUSDC = getReserveInUsd(w3, tlp, triUsdRatio, wnearUsdRatio, wethUsdRatio)
    totalSupply = tlp.functions.totalSupply().call()
    totalStaked = tlp.functions.balanceOf(chef.address).call()
    totalStakedInUSD = getTotalStakedInUSD(totalStaked, totalSupply, reserveInUSDC)
    totalSecondRewardRate = (
        triPerBlock * allocPoint / (totalAllocPoint * 10 ** tri_decimals)
    )  
    totalWeeklyRewardRate = (
        3600 * 24 * 7 * totalSecondRewardRate
    )
    return {
                "id": id,
                "poolId": id,
                "lpAddress": address,
                "totalSupply": totalSupply,
                "totalStaked": totalStaked,
                "totalStakedInUSD": totalStakedInUSD,
                "totalRewardRate": totalWeeklyRewardRate,
                # "totalWeeklyRewardRate": totalWeeklyRewardRate,
                "allocPoint": allocPoint,
                "apr": getAPR(triUsdRatio, totalSecondRewardRate, totalStakedInUSD),
                "apr2": 0,
                "chefVersion": "v1",
            }

def getDataV2Pools(w3, id, pool, chefv2, dummyLpTotalSecondRewardRate, totalAllocPointV2, triUsdRatio, wnearUsdRatio, wethUsdRatio):
    tlp = init_tlp(pool["LP"])
    poolInfo = chefv2.functions.poolInfo(id).call()
    allocPoint = poolInfo[2]
    totalSupply = tlp.functions.totalSupply().call()
    totalStaked = tlp.functions.balanceOf(chefv2.address).call()
    totalSecondRewardRate = (
            dummyLpTotalSecondRewardRate * allocPoint / (totalAllocPointV2)
    )  # Taking TRI allocation to dummy LP in chef v1 as tri per block for chef V2
    totalWeeklyRewardRate = (
        3600 * 24 * 7 * totalSecondRewardRate
    )

    # Rewarder logic
    rewardsPerBlock = 0
    doubleRewardUsdRatio = 0
    if pool["Rewarder"] != ZERO_ADDRESS:
        rewarder = init_rewarder(pool["Rewarder"])
        rewardDecimals = pool["RewarderTokenDecimals"]
        rewardsPerBlock = rewarder.functions.tokenPerBlock().call()/(10**rewardDecimals)
        rewarder_address = rewarder.functions.rewardToken().call()
        print(f"Double rewards per block: {rewardsPerBlock}")
        doubleRewardUsdRatio = getTokenUSDRatio(w3, pool, rewarder_address, wnearUsdRatio, triUsdRatio)    
        
    # Stable AMM LP staked amts logic
    if id == 18:
        stable_pool_contract = init_stable_pool(V2_STABLEPOOL_FACTORY[id]["poolContract"])
        virtual_price = stable_pool_contract.functions.getVirtualPrice().call()
        totalStakedInUSDC = (virtual_price/1e18) * (totalStaked/1e18)
    else:
        # Normal AMM LP staked amts logic
        reserveInUSDC = getReserveInUsd(w3, tlp, triUsdRatio, wnearUsdRatio, wethUsdRatio)
        totalStakedInUSDC = getTotalStakedInUSD(totalStaked, totalSupply, reserveInUSDC)

    return {
                "id": len(V1_POOLS) + id,
                "poolId": id,
                "lpAddress": pool["LP"],
                "totalSupply": totalSupply,
                "totalStaked": totalStaked,
                "totalStakedInUSD": totalStakedInUSDC,
                "totalRewardRate": totalWeeklyRewardRate,
                "allocPoint": allocPoint,
                "apr": getAPR(triUsdRatio, totalSecondRewardRate, totalStakedInUSDC),
                "apr2": getAPR(doubleRewardUsdRatio, rewardsPerBlock, totalStakedInUSDC),
                "chefVersion": "v2",
            }