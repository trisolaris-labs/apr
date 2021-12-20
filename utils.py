import json

FACTORY_ADDRESS = "0xc66F594268041dB60507F00703b152492fb176E7"
TRIMAKER_ADDRESS = "0xe793455c9728fc91A3E5a33FAfF9eB2F228aE151"
TRIBAR_ADDRESS = "0x802119e4e253D5C19aA06A5d567C5a41596D6803"
CHEF_ADDRESS = "0x1f1Ed214bef5E83D8f5d0eB5D7011EB965D0D79B"
CHEFV2_ADDRESS = "0x3838956710bcc9D122Dd23863a0549ca8D5675D6"
TRI_ADDRESS = "0xFa94348467f64D5A457F75F8bc40495D33c65aBB"
WNEAR_ADDRESS = "0xC42C30aC6Cc15faC9bD938618BcaA1a1FaE8501d"
AURORA_ADDRESS = "0x8BEc47865aDe3B172A928df8f990Bc7f2A3b9f79"
USDC_ADDRESS = "0xB12BFcA5A55806AaF64E99521918A4bf0fC40802"
USDT_ADDRESS = "0x4988a896b1227218e4A686fdE5EabdcAbd91571f"
WETH_ADDRESS = "0xC9BdeEd33CD01541e1eeD10f90519d2C06Fe3feB"
WBTC_ADDRESS = "0xF4eB217Ba2454613b15dBdea6e5f22276410e89e"


### TLP addresses
WNEAR_USDC = "0x20F8AeFB5697B77E0BB835A8518BE70775cdA1b0"
WETH_USDC = "0x2F41AF687164062f118297cA10751F4b55478ae1"
WNEAR_TRI = "0x84b123875F0F36B966d0B6Ca14b31121bd9676AD"
TRI_AURORA = "0xd1654a7713617d41A8C9530Fb9B948d00e162194"


def init_chef(w3):
    with open('abi/chef.json') as json_file:
        return w3.eth.contract(
            address=CHEF_ADDRESS,
            abi=json.load(json_file)
        )

def init_chefv2(w3):
    with open('abi/chefv2.json') as json_file:
        return w3.eth.contract(
            address=CHEFV2_ADDRESS,
            abi=json.load(json_file)
        )

def init_rewarder(w3, rewarderAddress):
    with open('abi/complexrewarder.json') as json_file:
        return w3.eth.contract(
            address=rewarderAddress,
            abi=json.load(json_file)
        )

def init_tlp(w3, lpAddress):
    with open('abi/tlp.json') as json_file:
        return w3.eth.contract(
            address=lpAddress,
            abi=json.load(json_file)
        )

def init_tri_maker(w3):
    with open('abi/triMaker.json') as json_file:
        return w3.eth.contract(
            address=TRIMAKER_ADDRESS,
            abi=json.load(json_file)
        )

def init_erc20(w3, erc20_address):
    with open('abi/erc20.json') as json_file:
        return w3.eth.contract(
            address=erc20_address,
            abi=json.load(json_file)
        )


def getReserveInUsdc(w3, tlp, triUsdcRatio):
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
    elif (t0 == TRI_ADDRESS or t1 == TRI_ADDRESS):
        print("reached here")
        if t0 == TRI_ADDRESS:
            reserveInTri = reserves[0]*2
        else:
            reserveInTri = reserves[1]*2
        print(reserveInTri, triUsdcRatio)
        return reserveInTri/triUsdcRatio


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
    return triWnearRatio * wnearUsdcRatio

def getAuroraUsdcRatio(w3):
    triAuroraPair = init_tlp(w3, TRI_AURORA)
    t1 = triAuroraPair.functions.token1().call()
    t0 = triAuroraPair.functions.token0().call()
    reserves = triAuroraPair.functions.getReserves().call()
    if t0 == TRI_ADDRESS:
        triAuroraRatio = reserves[1]/reserves[0]
    else:
        triAuroraRatio = reserves[0]/reserves[1]
    
    triUsdcRatio = getTriUsdcRatio(w3)
    return triAuroraRatio * triUsdcRatio

def getAPR(triUsdRatio, totalRewardRate, totalStakedInUSDC):
    if totalStakedInUSDC == 0:
        return 0
    else:
        totalYearlyRewards = totalRewardRate * 3600 * 24 * 365
        return totalYearlyRewards*100*10**6/(totalStakedInUSDC*triUsdRatio)

def convertFeesForPair(tri_maker, pair, w3, acct):
    transaction = {
    'gasPrice': w3.eth.gas_price,
    'nonce': w3.eth.getTransactionCount(acct.address),
    }
    convert_tranasction = tri_maker.functions.convert(pair[0], pair[1]).buildTransaction(transaction)
    signed = w3.eth.account.sign_transaction(convert_tranasction, acct.key)
    signed_txn = w3.eth.sendRawTransaction(signed.rawTransaction)
    txn_hash = signed_txn.hex()
    return w3.eth.waitForTransactionReceipt(txn_hash, timeout=1200)
