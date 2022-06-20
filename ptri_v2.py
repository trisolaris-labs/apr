import json
from ptri_base_v2 import ptri_base_v2


def ptri_v2():
    print("Starting pTRI V2")

    timestamp = None
    with open("ptri_v2.json") as json_file:
        data = json.load(json_file)
        timestamp = data[-1]["timestamp"]
    result = ptri_base_v2(timestamp)
    data.append(result)

    with open("ptri_v2.json", "w", encoding="utf-8") as f:
        if len(data) < 7:
            json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            json.dump(data[-7:], f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    ptri_base_v2()
