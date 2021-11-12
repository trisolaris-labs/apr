import json

FACTORY_ADDRESS = "0xc66F594268041dB60507F00703b152492fb176E7"
CHEF_ADDRESS = "0x474b825a605c45836Ac50398473059D4c4c6d3Db"
WETH_ADDRESS = "0xC9BdeEd33CD01541e1eeD10f90519d2C06Fe3feB"
WNEAR_ADDRESS = "0xC42C30aC6Cc15faC9bD938618BcaA1a1FaE8501d"
USDC_ADDRESS = "0xB12BFcA5A55806AaF64E99521918A4bf0fC40802"
TRI_ADDRESS = "0x0029050f71704940D77Cfe71D0F1FB868DeeFa03"
DAI_ADDRESS = "0xe3520349f477a5f6eb06107066048508498a291b"

DAI_USDC = "0xbb310Ef4Fac855f2F49D8Fb35A2DA8f639B3464E"
WNEAR_USDC = "0x20F8AeFB5697B77E0BB835A8518BE70775cdA1b0"
TRI_USDC = "0x56ff686187cffbB09E545655F88CCaB690D77cE2"


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

def getAPR(w3, totalRewardRate, totalStakedInUSDC):
    if totalStakedInUSDC == 0:
        return 0
    else:
        triUsdcPair = init_tlp(w3, TRI_USDC)
        t0 = triUsdcPair.functions.token0().call()
        t1 = triUsdcPair.functions.token1().call()
        reserves = triUsdcPair.functions.getReserves().call()
        if t0 == USDC_ADDRESS:
            triUSDCRatio = reserves[1]/reserves[0]
        else:
            triUSDCRatio = reserves[0]/reserves[1]
        totalYearlyRewards = totalRewardRate * 3600 * 24 * 365
        return triUSDCRatio*totalYearlyRewards*100/(totalStakedInUSDC * 10**6)
