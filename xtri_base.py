from time import sleep, time

from utils.constants import (
    ASHIBAM_ADDRESS,
    ATLUNA_ADDRESS,
    ATUST_ADDRESS,
    AURORA_ADDRESS,
    TRI_ADDRESS,
    TRIBAR_ADDRESS,
    USDC_ADDRESS,
    USDT_ADDRESS,
    WBTC_ADDRESS,
    WETH_ADDRESS,
    WNEAR_ADDRESS,
)
from utils.fees import convertFeesForPair, getAccount, getFundedAccount
from utils.node import init_erc20, init_tri_maker, w3

pairs = [
    (ATLUNA_ADDRESS, WNEAR_ADDRESS),
    (ATUST_ADDRESS, WNEAR_ADDRESS),
    (USDC_ADDRESS, WNEAR_ADDRESS),
    (USDT_ADDRESS, WNEAR_ADDRESS),
    (WBTC_ADDRESS, WNEAR_ADDRESS),
    (TRI_ADDRESS, WNEAR_ADDRESS),
    (TRI_ADDRESS, USDC_ADDRESS),
    (TRI_ADDRESS, USDT_ADDRESS),
    (AURORA_ADDRESS, TRI_ADDRESS),
    (WETH_ADDRESS, TRI_ADDRESS),
    (WETH_ADDRESS, WNEAR_ADDRESS),
    (WETH_ADDRESS, USDC_ADDRESS),
    (WETH_ADDRESS, USDT_ADDRESS),
    (AURORA_ADDRESS, WETH_ADDRESS),
    (ASHIBAM_ADDRESS, WETH_ADDRESS),
    (USDC_ADDRESS, USDT_ADDRESS),
]

TAG = "[GCC_XTRI_BASE] "


def xtri_base(timestamp):
    try:
        # 2/8/22 - Total cost of a complete run is 0.00016Ξ
        acct = getFundedAccount()
    except Exception as ex:
        print(
            TAG
            + "Error getting funded account: "
            + str(ex)
            + "\n"
            + "Using temp mnemonic"
        )
        temp_mnemonic = "test test test test test test test test test test test junk"
        acct = getAccount(temp_mnemonic)

    print("xtri acct balance: " + str(w3.eth.get_balance(acct.address) / 1e18) + "Ξ")

    tri_maker = init_tri_maker()
    tri = init_erc20(TRI_ADDRESS)

    tri_amount = 0
    initial_triBar_balance = tri.functions.balanceOf(TRIBAR_ADDRESS).call()
    current_time = time()

    xtri_data = {}

    for pair in pairs:
        sleep(5)
        tri_amount += convertFeesForPair(tri_maker, pair, w3, acct)
        print(TAG, "tri_amount: ", tri_amount)

    print(TAG, current_time, initial_triBar_balance, tri_amount)

    if timestamp != 0 and timestamp is not None:
        timedelta = current_time - timestamp
        pr = tri_amount / initial_triBar_balance
        apr = pr * (3600 * 24 * 365) * 100 / timedelta
        xtri_data["apr"] = apr

    xtri_data["triBarTri"] = initial_triBar_balance
    xtri_data["mintedTri"] = tri_amount
    xtri_data["timestamp"] = current_time

    return xtri_data
