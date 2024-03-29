import os
import requests
from urllib import parse
import time
from .constants import (
    TRI_ADDRESS,
    USDC_ADDRESS,
    WNEAR_ADDRESS,
    USDT_ADDRESS,
    TRIBAR_ADDRESS,
    ZERO_ADDRESS,
)
from .node import init_aurigami_erc20, init_erc20, init_tlp


def is_prefixed_with_0x(input_string):
    return input_string[:2] == "0x"


def getTokenUSDRatio(
    w3, pool, reward_token_address, wnearUsdRatio, triUsdRatio, i=None
):
    if pool["Rewarder"] == ZERO_ADDRESS:
        return 0
    elif pool["CoingeckoRewarderTokenName"] != "":
        return getCoingeckoUSDPriceRatio(pool["CoingeckoRewarderTokenName"])
    elif pool.get("RewarderPriceLPs") and i is not None:
        reward_token_price_source = pool["RewarderPriceLPs"][i]

        if len(reward_token_price_source) == 42 and is_prefixed_with_0x(
            reward_token_price_source
        ):
            return getDexTokenUSDRatio(
                w3,
                reward_token_price_source,
                reward_token_address,
                wnearUsdRatio,
                triUsdRatio,
            )
        else:
            return getCoingeckoUSDPriceRatio(reward_token_price_source)
    else:
        return getDexTokenUSDRatio(
            w3,
            pool["RewarderPriceLP"],
            reward_token_address,
            wnearUsdRatio,
            triUsdRatio,
        )


# Takes a TLP token with either USDC, USDT or WNEAR and returns the token price in USD
# NOTE: the prices are returned in USD and NOT USDC
def getDexTokenUSDRatio(
    w3, tlp_address, reward_token_address, wnearUsdRatio=0, triUsdRatio=0
):
    ## getting token reserve ratio
    pair = init_tlp(tlp_address)
    t1 = pair.functions.token1().call()
    t1_decimals = init_erc20(t1).functions.decimals().call()
    t0 = pair.functions.token0().call()
    t0_decimals = init_erc20(t0).functions.decimals().call()
    reserves = pair.functions.getReserves().call()
    if t0 == reward_token_address:
        tokenReserveRatio = (
            reserves[0] * (10 ** (t1_decimals - t0_decimals)) / reserves[1]
        )
    else:
        tokenReserveRatio = (
            reserves[1] * (10 ** (t0_decimals - t1_decimals)) / reserves[0]
        )

    ## Converting it into price
    if (
        t1 == USDC_ADDRESS
        or t0 == USDC_ADDRESS
        or t1 == USDT_ADDRESS
        or t0 == USDT_ADDRESS
    ):
        return tokenReserveRatio
    elif t1 == WNEAR_ADDRESS or t0 == WNEAR_ADDRESS:
        return tokenReserveRatio * wnearUsdRatio
    elif t1 == TRI_ADDRESS or t0 == TRI_ADDRESS:
        return tokenReserveRatio * triUsdRatio
    else:
        raise ValueError("TLP does not have wnear, tri or usd as base token")


def getCoingeckoUSDPriceRatio(asset, retries=3, retry_delay=5):
    try_count = 0
    while try_count < retries:
        try:
            coingecko_api_key = os.getenv("COINGECKO_API_KEY")
            coingecko_query_params = {"ids": asset, "vs_currencies": "usd"}

            if coingecko_api_key:
                coingecko_query_params["x_cg_pro_api_key"] = coingecko_api_key
                coingecko_api_endpoint_root = (
                    "https://pro-api.coingecko.com/api/v3/simple/price"
                )
            else:
                coingecko_api_endpoint_root = (
                    "https://api.coingecko.com/api/v3/simple/price"
                )

            coingecko_encoded_query_params = parse.urlencode(
                coingecko_query_params, doseq=False
            )
            coingecko_api_endpoint = (
                f"{coingecko_api_endpoint_root}?{coingecko_encoded_query_params}"
            )

            response = requests.get(coingecko_api_endpoint)
            response_json = response.json()

            if asset in response_json and "usd" in response_json[asset]:
                usd_price = response_json[asset]["usd"]
                return 1 / usd_price
            else:
                print(f"Invalid response format for asset: {asset}")
                print(response_json)
                raise ValueError(f"Invalid response format for asset: {asset}")

        except Exception as e:
            try_count += 1
            if try_count < retries:
                print(f"Coingecko API Call Error (Attempt {try_count}): {e}")
                time.sleep(retry_delay)
            else:
                print(f"Max retry attempts reached. Coingecko API Call Error: {e}")
                return 0


def getTriXTriRatio(w3):
    xtri = init_erc20(TRIBAR_ADDRESS)
    tri = init_erc20(TRI_ADDRESS)
    xtri_supply = xtri.functions.totalSupply().call()
    tri_locked = tri.functions.balanceOf(TRIBAR_ADDRESS).call()
    return tri_locked / xtri_supply


def getAurigamiERC20ExchangeRate(au_erc20_address):
    au_token = init_aurigami_erc20(au_erc20_address)
    au_token_exchange_rate = au_token.functions.exchangeRateStored().call()
    return au_token_exchange_rate / 1e16
