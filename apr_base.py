from utils.constants import (
    TRI_ADDRESS,
    V1_POOLS,
    V2_POOLS,
    WETH_ADDRESS,
    WETH_USDC,
    WNEAR_ADDRESS,
    WNEAR_TRI,
    WNEAR_USDC,
)
from utils.node import init_chef, init_chefv2, w3
from utils.prices import getDexTokenUSDRatio
from utils.reserves import getDataV1Pools, getDataV2Pools


def apr_base():
    print("Starting APR BASE")
    data = []

    ## chef data
    tri_decimals = 18
    chef = init_chef()
    totalAllocPoint = chef.functions.totalAllocPoint().call()
    triPerBlock = chef.functions.triPerBlock().call()

    ## chefv2 calls
    dummyLPPoolId = 7
    dummyLPToken = "0x9990a658F71248cc507Ea62946f0EB7728491B70"
    dummyLpPoolInfo = chef.functions.poolInfo(dummyLPPoolId).call()
    assert dummyLpPoolInfo[0].lower() == dummyLPToken.lower()
    dummyLpAllocPoint = dummyLpPoolInfo[1]
    dummyLpTotalSecondRewardRate = (
        triPerBlock * dummyLpAllocPoint / (totalAllocPoint * 10**tri_decimals)
    )

    # Chef V2 calls
    chefv2 = init_chefv2()
    totalAllocPointV2 = chefv2.functions.totalAllocPoint().call()

    ### Getting initial prices
    wnearUsdRatio = getDexTokenUSDRatio(w3, WNEAR_USDC, WNEAR_ADDRESS)
    wethUsdRatio = getDexTokenUSDRatio(w3, WETH_USDC, WETH_ADDRESS)
    triUsdRatio = getDexTokenUSDRatio(w3, WNEAR_TRI, TRI_ADDRESS, wnearUsdRatio)

    for id, address in V1_POOLS.items():
        print("V1 Reached here", address)
        # Chef V1
        data.append(
            getDataV1Pools(
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
            )
        )

    for id, pool in V2_POOLS.items():
        print(f"V2 Reached here {id}: {pool['LP']}")
        data.append(
            getDataV2Pools(
                w3,
                id,
                pool,
                chefv2,
                dummyLpTotalSecondRewardRate,
                totalAllocPointV2,
                triUsdRatio,
                wnearUsdRatio,
                wethUsdRatio,
            )
        )
    return data


if __name__ == "__main__":
    apr_base()
