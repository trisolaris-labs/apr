from gcc_utils import gccPrint
from utils.covalent import getPool
from .node import (
    init_erc20,
    init_n_rewarder,
    init_rewarder,
    init_stable_pool,
    init_tlp,
)
from .constants import (
    AURIGAMI_USDC_ADDRESS,
    COINGECKO_TOKEN_ID_MAP,
    USDC_ADDRESS,
    USDT_ADDRESS,
    WNEAR_ADDRESS,
    WETH_ADDRESS,
    TRI_ADDRESS,
    TRIBAR_ADDRESS,
    XNL_ADDRESS,
    ZERO_ADDRESS,
    V1_POOLS,
    V2_STABLEPOOL_METADATA,
)
from .prices import (
    getAurigamiERC20ExchangeRate,
    getCoingeckoUSDPriceRatio,
    getTriXTriRatio,
    getTokenUSDRatio,
)


# have function that gets balance of underlying tokens, and then multiply 1
# add value and then get reserve
# LP token address does not hold tokens, other address does so need both
def getReserveStables(w3, total_supply, address):
    stable_pool_contract = init_stable_pool(address)
    virtual_price = stable_pool_contract.functions.getVirtualPrice().call()
    reserve = (virtual_price * total_supply) / (10**36)
    return reserve


def getReserveInUsd(w3, tlp, triUsdRatio, wnearUsdRatio, wethUsdRatio):
    t0 = tlp.functions.token0().call()
    t1 = tlp.functions.token1().call()
    reserves = tlp.functions.getReserves().call()
    if t0 == USDC_ADDRESS or t1 == USDC_ADDRESS:
        decimals = init_erc20(USDC_ADDRESS).functions.decimals().call()
        if t0 == USDC_ADDRESS:
            return reserves[0] * 2 / 10**decimals
        else:
            return reserves[1] * 2 / 10**decimals
    elif t0 == WNEAR_ADDRESS or t1 == WNEAR_ADDRESS:
        decimals = init_erc20(WNEAR_ADDRESS).functions.decimals().call()
        if t0 == WNEAR_ADDRESS:
            reserveInWnear = reserves[0] * 2 / 10**decimals
        else:
            reserveInWnear = reserves[1] * 2 / 10**decimals
        return reserveInWnear / wnearUsdRatio
    elif t0 == WETH_ADDRESS or t1 == WETH_ADDRESS:
        decimals = init_erc20(WETH_ADDRESS).functions.decimals().call()
        if t0 == WETH_ADDRESS:
            reserveInWeth = reserves[0] * 2 / 10**decimals
        else:
            reserveInWeth = reserves[1] * 2 / 10**decimals
        return reserveInWeth / wethUsdRatio
    elif t0 == TRI_ADDRESS or t1 == TRI_ADDRESS:
        decimals = init_erc20(TRI_ADDRESS).functions.decimals().call()
        if t0 == TRI_ADDRESS:
            reserveInTri = reserves[0] * 2 / 10**decimals
        else:
            reserveInTri = reserves[1] * 2 / 10**decimals
        return reserveInTri / triUsdRatio
    elif t0 == TRIBAR_ADDRESS or t1 == TRIBAR_ADDRESS:
        decimals = init_erc20(TRIBAR_ADDRESS).functions.decimals().call()
        if t0 == TRIBAR_ADDRESS:
            reserveInXTri = reserves[0] * 2 / 10**decimals
        else:
            reserveInXTri = reserves[1] * 2 / 10**decimals
        return reserveInXTri * getTriXTriRatio(w3) / triUsdRatio
    elif t0 == XNL_ADDRESS or t1 == XNL_ADDRESS:
        decimals = init_erc20(XNL_ADDRESS).functions.decimals().call()
        if t0 == XNL_ADDRESS:
            reserveInTri = reserves[0] * 2 / 10**decimals
        else:
            reserveInTri = reserves[1] * 2 / 10**decimals
        return reserveInTri / triUsdRatio
    elif t0 == USDT_ADDRESS or t1 == USDT_ADDRESS:
        decimals = init_erc20(USDT_ADDRESS).functions.decimals().call()
        if t0 == USDT_ADDRESS:
            return reserves[0] * 2 / 10**decimals
        else:
            return reserves[1] * 2 / 10**decimals
    elif t0 in COINGECKO_TOKEN_ID_MAP or t1 in COINGECKO_TOKEN_ID_MAP:
        # Attempt to get reserves using CoinGecko API
        reference_token_address = t0 if t0 in COINGECKO_TOKEN_ID_MAP else t1
        reference_token_ID = COINGECKO_TOKEN_ID_MAP[reference_token_address]
        reference_token_usd_ratio = getCoingeckoUSDPriceRatio(reference_token_ID)
        reference_token_decimals = (
            init_erc20(reference_token_address).functions.decimals().call()
        )
        if t0 == reference_token_address:
            reserveInTri = reserves[0] * 2 / 10**reference_token_decimals
        else:
            reserveInTri = reserves[1] * 2 / 10**reference_token_decimals
        return reserveInTri / reference_token_usd_ratio
    else:
        # Attempt to get reserves from Covalent API
        covalent_response = getPool(tlp.address)

        if covalent_response is not None:
            return covalent_response["total_liquidity_quote"]

        return 0


def getTotalStakedInUSD(totalStaked, totalAvailable, reserveInUSD):
    if totalAvailable == 0:
        return 0
    else:
        return totalStaked * reserveInUSD / totalAvailable


def getAPR(tokenUsdRatio, totalRewardRate, totalStakedInUSD):
    if totalStakedInUSD == 0 or tokenUsdRatio == 0:
        return 0
    else:
        totalYearlyRewards = totalRewardRate * 3600 * 24 * 365
        return totalYearlyRewards * 100 / (totalStakedInUSD * tokenUsdRatio)


def getDataV1Pools(
    w3,
    id,
    address,
    chef,
    triPerBlock,
    totalAllocPoint,
    tri_decimals,
    triUsdRatio,
    wnearUsdRatio,
    wethUsdRatio,
):
    tlp = init_tlp(address)
    poolInfo = chef.functions.poolInfo(id).call()
    assert poolInfo[0].lower() == address.lower()
    allocPoint = poolInfo[1]
    reserveInUSDC = getReserveInUsd(w3, tlp, triUsdRatio, wnearUsdRatio, wethUsdRatio)
    totalSupply = tlp.functions.totalSupply().call()
    totalStaked = tlp.functions.balanceOf(chef.address).call()
    totalStakedInUSD = getTotalStakedInUSD(totalStaked, totalSupply, reserveInUSDC)
    totalSecondRewardRate = (
        triPerBlock * allocPoint / (totalAllocPoint * 10**tri_decimals)
    )
    totalWeeklyRewardRate = 3600 * 24 * 7 * totalSecondRewardRate
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
        "nonTriAPRs": [],
        "chefVersion": "v1",
    }


def getDataV2Pools(
    w3,
    id,
    pool,
    chefv2,
    dummyLpTotalSecondRewardRate,
    totalAllocPointV2,
    triUsdRatio,
    wnearUsdRatio,
    wethUsdRatio,
):
    tlp = init_tlp(pool["LP"])
    poolInfo = chefv2.functions.poolInfo(id).call()
    allocPoint = poolInfo[2]
    totalSupply = tlp.functions.totalSupply().call()
    totalStaked = tlp.functions.balanceOf(chefv2.address).call()
    totalSecondRewardRate = (
        dummyLpTotalSecondRewardRate * allocPoint / (totalAllocPointV2)
    )  # Taking TRI allocation to dummy LP in chef v1 as tri per block for chef V2
    totalWeeklyRewardRate = 3600 * 24 * 7 * totalSecondRewardRate

    # Stable AMM LP staked amts logic
    if pool["LPType"] == "StableAMM":
        stable_pool_contract = init_stable_pool(
            V2_STABLEPOOL_METADATA[id]["poolContract"]
        )

        if V2_STABLEPOOL_METADATA[id]["referenceToken"] == USDC_ADDRESS:
            reference_token_price = getCoingeckoUSDPriceRatio("usd-coin")
        elif V2_STABLEPOOL_METADATA[id]["referenceToken"] == AURIGAMI_USDC_ADDRESS:
            reference_token_price = getAurigamiERC20ExchangeRate(AURIGAMI_USDC_ADDRESS)

        virtual_price = stable_pool_contract.functions.getVirtualPrice().call()
        # Multiply virtual price by reference token to get USD value of LP token, relative to underlying assets
        normalized_virtual_price = virtual_price * reference_token_price
        totalStakedInUSDC = (normalized_virtual_price / 1e18) * (totalStaked / 1e18)
    else:
        # Normal AMM LP staked amts logic
        reserveInUSDC = getReserveInUsd(
            w3, tlp, triUsdRatio, wnearUsdRatio, wethUsdRatio
        )
        if reserveInUSDC > 0:
            totalStakedInUSDC = getTotalStakedInUSD(
                totalStaked, totalSupply, reserveInUSDC
            )
        else:
            gccPrint(f'Error getting reserveInUSDC for pair {pool["LP"]}', "ERROR")
            totalStakedInUSDC = 0

    nonTriAPRs = []

    # Rewarder logic
    if pool["Rewarder"] != ZERO_ADDRESS:
        if pool["RewarderType"] == "Complex":
            rewardsPerBlockForItem = 0
            tokenUsdRatio = 0
            rewarderContractForItem = init_n_rewarder(pool["Rewarder"])
            numRewardTokens = rewarderContractForItem.functions.numRewardTokens().call()

            for i in range(numRewardTokens):
                rewardTokenAddressForItem = (
                    rewarderContractForItem.functions.rewardTokens(i).call()
                )
                rewardTokenContractForItem = init_erc20(rewardTokenAddressForItem)
                rewardDecimalsForItem = (
                    rewardTokenContractForItem.functions.decimals().call()
                )

                rewardsPerBlockForItem = (
                    rewarderContractForItem.functions.tokenPerBlock(i).call()
                    / (10**rewardDecimalsForItem)
                )

                print(
                    f"Complex N rewards per block at index {i}: {rewardsPerBlockForItem}"
                )
                tokenUsdRatio = getTokenUSDRatio(
                    w3, pool, rewardTokenAddressForItem, wnearUsdRatio, triUsdRatio
                )

                nonTriAPRs.append(
                    {
                        "address": rewardTokenAddressForItem,
                        "apr": getAPR(
                            tokenUsdRatio,
                            rewardsPerBlockForItem,
                            totalStakedInUSDC,
                        ),
                    }
                )

        elif pool["RewarderType"] == "Simple":
            rewardsPerBlockForItem = 0
            tokenUsdRatio = 0
            rewarderContractForItem = init_rewarder(pool["Rewarder"])
            rewardDecimalsForItem = pool["RewarderTokenDecimals"]
            rewardsPerBlockForItem = (
                rewarderContractForItem.functions.tokenPerBlock().call()
                / (10**rewardDecimalsForItem)
            )
            rewardTokenAddressForItem = (
                rewarderContractForItem.functions.rewardToken().call()
            )

            print(f"Double rewards per block: {rewardsPerBlockForItem}")
            tokenUsdRatio = getTokenUSDRatio(
                w3, pool, rewardTokenAddressForItem, wnearUsdRatio, triUsdRatio
            )

            nonTriAPRs.append(
                {
                    "address": rewardTokenAddressForItem,
                    "apr": getAPR(
                        tokenUsdRatio,
                        rewardsPerBlockForItem,
                        totalStakedInUSDC,
                    ),
                }
            )

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
        "nonTriAPRs": nonTriAPRs,
        "chefVersion": "v2",
    }
