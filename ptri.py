import json
from ptri_base import ptri_base

def ptri():
    print("Starting pTRI")

    timestamp = None
    with open('ptri.json') as json_file:
         data = json.load(json_file)
         timestamp = data[-1]['timestamp']
    result = ptri_base(timestamp)
    data.append(result)

    with open("ptri.json", "w", encoding="utf-8") as f:
        if len(data) < 7:
            json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            json.dump(data[-7:], f, ensure_ascii=False, indent=4)
        


if __name__ == "__main__":
    ptri()