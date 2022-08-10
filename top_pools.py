import json
from gcc_utils import gccPrint
from top_pools_base import top_pools_base
from utils.node import getTokenSymbol


def top_pools():
    print("Starting top pools")

    top_pool_tokens = top_pools_base()

    with open("pools.json", "w", encoding="utf-8") as f:
        json.dump(top_pool_tokens, f, ensure_ascii=False, indent=4)

    gccPrint("Top Pools populated with:")
    for pair in top_pool_tokens:
        gccPrint(f'\t {":".join(map(getTokenSymbol, pair))}')


if __name__ == "__main__":
    top_pools()
