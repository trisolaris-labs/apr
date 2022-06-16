## APR

This repo is used to perform offchain calculations, these calculations are deployed on GCP functions

## Dependencies

python3 version 3.7.2 or greater, python3-dev

### Setup via setuptools

You can clone the repository and use setuptools for the most up-to-date version:

git clone https://github.com/trisolaris-labs/apr.git
cd apr
python3 -m venv venv
pip install -e .
pip install -e '.[dev]'

### How to add a new APR to cloud function

The only thing that needs to be done to add a new pool for APR calculation is add a new dictionary in the `V2_POOLS` array [here](https://github.com/trisolaris-labs/apr/blob/9934411f39dca9ca9391fb79768ba7b9e3d09fe9/utils/constants.py#L239)

Sample

```
        23: {
            "LP": "0xBBf3D4281F10E537d5b13CA80bE22362310b2bf9",
            "LPType": "",
            "Rewarders": {
                    0: {
                        "Rewarder": "0xDc6d09f5CC085E29972d192cB3AdCDFA6495a741",
                        "CoingeckoRewarderTokenName": "",
                        "RewarderPriceLP": BSTN_WNEAR,
                        "RewarderTokenDecimals": 18,
                    }
                }
            }
```

- The first number signifies the ID of the pool in ChefV2
- **LP**: key signifies the LP address which is being incentivized
- **LPType**: signifies if its a StableAMM of not
- **Rewarder**: signifies the rewarder address for v2 rewards, put a zero address fif there is no dual rewarder
- **CoingeckoRewarderTokenName**: Is the coingecko token name of the rewarder token. This is to get the price of the rewarder token from Coingecko. Leave it empty if we need to get the price from the dex.
- **RewarderPriceLP**: Is the LP address one of its tokens SHOULD be the rewarder token and the second should be one of either USDC, USDT, WNEAR or TRI. This LP will be used to determine the price of rewarder token if `CoingeckoRewarderTokenName` is empty.
- **RewarderTokenDecimals**: Are the decimals in the rewarder token.
