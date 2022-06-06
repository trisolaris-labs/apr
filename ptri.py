import json
from ptri_base import ptri_base

def ptri():
    print("Starting pTRI")

    data = ptri_base(None)

    with open("ptri.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    ptri()