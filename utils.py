import json

FACTORY_ADDRESS = "0xc66F594268041dB60507F00703b152492fb176E7"
CHEF_ADDRESS = "0x1f1Ed214bef5E83D8f5d0eB5D7011EB965D0D79B"
WNEAR_ADDRESS = "0xC42C30aC6Cc15faC9bD938618BcaA1a1FaE8501d"
USDC_ADDRESS = "0xB12BFcA5A55806AaF64E99521918A4bf0fC40802"

WNEAR_USDC = "0x20F8AeFB5697B77E0BB835A8518BE70775cdA1b0"
# TODO: change this address
WNEAR_TRI = "0xD4B28eA361DF98568FF65dD3e60407c3fBC014A7"


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

def getTotalStakedInUSDC(totalStaked, totalAvailable, reserveInUSDC):
    if totalAvailable == 0:
        return 0
    else:
        return totalStaked*reserveInUSDC/totalAvailable

def getTriUsdcRatio(w3):
    triWnearPair = init_tlp(w3, WNEAR_TRI)
    t0 = triWnearPair.functions.token0().call()
    reserves = triWnearPair.functions.getReserves().call()
    if t0 == WNEAR_ADDRESS:
        triWnearRatio = reserves[1]/reserves[0]
    else:
        triWnearRatio = reserves[0]/reserves[1]
        
    usdcWnearPair = init_tlp(w3, WNEAR_USDC)
    t0 = usdcWnearPair.functions.token0().call()
    reserves = usdcWnearPair.functions.getReserves().call()
    if t0 == WNEAR_ADDRESS:
        wnearUsdcRatio = reserves[0]/reserves[1]
    else:
        wnearUsdcRatio = reserves[1]/reserves[0]
    return triWnearRatio * wnearUsdcRatio

def getAPR(triUsdRatio, totalRewardRate, totalStakedInUSDC):
    if totalStakedInUSDC == 0:
        return 0
    else:
        totalYearlyRewards = totalRewardRate * 3600 * 24 * 365
        return triUsdRatio*totalYearlyRewards*100*10**6/(totalStakedInUSDC)
