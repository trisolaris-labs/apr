import json
from top_pools_base import top_pools_base

default_frequency = 24

def top_pools():
    print("Starting top pools")

    top_pool_tokens = top_pools_base()

    with open("pools.json", "w", encoding="utf-8") as f:
        json.dump(top_pool_tokens, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    top_pools()