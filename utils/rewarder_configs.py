import requests
from retry import retry
from web3 import Web3

from utils.constants import ZERO_ADDRESS

REWARDER_CONFIG_ENDPOINT = "https://raw.githubusercontent.com/trisolaris-labs/trisolaris_core/main/rewarderConfigs.json"


@retry((Exception), delay=10, tries=5)
def getRewarderConfigs():
    rewarder_configs = []
    try:
        rewarder_configs = requests.get(REWARDER_CONFIG_ENDPOINT).json()
    except Exception as e:
        raise e

    return rewarder_configs


def formatRewarderConfigItem(rewarder_config_item):
    rewarder = _getOptionalValueFromRewarderConfigItem(
        rewarder_config_item, "Rewarder", ZERO_ADDRESS
    )
    coingecko_token_name = _getOptionalValueFromRewarderConfigItem(
        rewarder_config_item, "CoingeckoRewarderTokenName"
    )
    rewarder_price_lp = _getOptionalValueFromRewarderConfigItem(
        rewarder_config_item, "RewarderPriceLP"
    )

    id = rewarder_config_item["PoolId"]
    pool = {
        "LP": Web3.toChecksumAddress(rewarder_config_item["LPToken"]),
        "LPType": "",
        "Rewarder": rewarder,
        "CoingeckoRewarderTokenName": coingecko_token_name,
        "RewarderPriceLP": rewarder_price_lp,
        "RewarderTokenDecimals": rewarder_config_item["RewardTokenDecimals"],
    }

    return (id, pool)


def _getOptionalValueFromRewarderConfigItem(rewarder_config_item, key, fallback=""):
    if key not in rewarder_config_item:
        return fallback

    if rewarder_config_item[key] is None or "":
        return fallback

    return rewarder_config_item[key]
