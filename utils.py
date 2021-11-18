import json

FACTORY_ADDRESS = "0xc66F594268041dB60507F00703b152492fb176E7"
CHEF_ADDRESS = "0x1f1Ed214bef5E83D8f5d0eB5D7011EB965D0D79B"
WNEAR_ADDRESS = "0xC42C30aC6Cc15faC9bD938618BcaA1a1FaE8501d"
USDC_ADDRESS = "0xB12BFcA5A55806AaF64E99521918A4bf0fC40802"
WETH_ADDRESS = "0xC9BdeEd33CD01541e1eeD10f90519d2C06Fe3feB"

WNEAR_USDC = "0x20F8AeFB5697B77E0BB835A8518BE70775cdA1b0"
WETH_USDC = "0x2F41AF687164062f118297cA10751F4b55478ae1"
WNEAR_TRI = "0x84b123875F0F36B966d0B6Ca14b31121bd9676AD"


def init_chef(w3):
    with open('chef.json') as json_file:
        return w3.eth.contract(
            address=CHEF_ADDRESS,
            abi=json.load(json_file)
        )

def init_tlp(w3, lpAddress):
    with open('tlp.json') as json_file:
        return w3.eth.contract(
            address=lpAddress,
            abi=json.load(json_file)
        )


def getReserveInUsdc(w3, tlp):
    t0 = tlp.functions.token0().call()
    t1 = tlp.functions.token1().call()
    reserves = tlp.functions.getReserves().call()
    if (t0 == USDC_ADDRESS or t1 == USDC_ADDRESS):
        if t0 == USDC_ADDRESS:
            return reserves[0]*2
        else:
            return reserves[1]*2
    elif (t0 == WNEAR_ADDRESS or t1 == WNEAR_ADDRESS):
        wnearUsdcPair = init_tlp(w3, WNEAR_USDC)
        reservesWnearUsdc = wnearUsdcPair.functions.getReserves().call()
        t0WnearUsdc = wnearUsdcPair.functions.token0().call()
        if t0 == WNEAR_ADDRESS:
            reserveInWnear = reserves[0]*2
        else:
            reserveInWnear = reserves[1]*2
        if t0WnearUsdc == WNEAR_ADDRESS:
            wnearReserveInWNearUsdcPair = reservesWnearUsdc[0]
            usdcReserveInWNearUsdcPair = reservesWnearUsdc[1]
        else:
            wnearReserveInWNearUsdcPair = reservesWnearUsdc[1]
            usdcReserveInWNearUsdcPair = reservesWnearUsdc[0]
        return reserveInWnear*usdcReserveInWNearUsdcPair/wnearReserveInWNearUsdcPair
    elif (t0 == WETH_ADDRESS or t1 == WETH_ADDRESS):
        wethUsdcPair = init_tlp(w3, WETH_USDC)
        reservesWethUsdc = wethUsdcPair.functions.getReserves().call()
        t0WethUsdc = wethUsdcPair.functions.token0().call()
        if t0 == WETH_ADDRESS:
            reserveInWeth = reserves[0]*2
        else:
            reserveInWeth = reserves[1]*2
        if t0WethUsdc == WETH_ADDRESS:
            wethReserveInWethUsdcPair = reservesWethUsdc[0]
            usdcReserveInWethUsdcPair = reservesWethUsdc[1]
        else:
            wethReserveInWethUsdcPair = reservesWethUsdc[1]
            usdcReserveInWethUsdcPair = reservesWethUsdc[0]
        return reserveInWeth*usdcReserveInWethUsdcPair/wethReserveInWethUsdcPair

def getTotalStakedInUSDC(totalStaked, totalAvailable, reserveInUSDC):
    if totalAvailable == 0:
        return 0
    else:
        return totalStaked*reserveInUSDC/totalAvailable

def getTriUsdcRatio(w3):
    triWnearPair = init_tlp(w3, WNEAR_TRI)
    t1 = triWnearPair.functions.token1().call()
    t0 = triWnearPair.functions.token0().call()
    reserves = triWnearPair.functions.getReserves().call()
    if t0 == WNEAR_ADDRESS:
        triWnearRatio = reserves[1]/reserves[0]
    else:
        triWnearRatio = reserves[0]/reserves[1]
    
    usdcWnearPair = init_tlp(w3, WNEAR_USDC)
    t1 = usdcWnearPair.functions.token1().call()
    t0 = usdcWnearPair.functions.token0().call()
    reserves = usdcWnearPair.functions.getReserves().call()

    if t0 == WNEAR_ADDRESS:
        wnearUsdcRatio = reserves[0]/reserves[1]
    else:
        wnearUsdcRatio = reserves[1]/reserves[0]
    print(triWnearRatio, wnearUsdcRatio)
    return triWnearRatio * wnearUsdcRatio

def getAPR(triUsdRatio, totalRewardRate, totalStakedInUSDC):
    if totalStakedInUSDC == 0:
        return 0
    else:
        totalYearlyRewards = totalRewardRate * 3600 * 24 * 365
        return totalYearlyRewards*100*10**6/(totalStakedInUSDC*triUsdRatio)
