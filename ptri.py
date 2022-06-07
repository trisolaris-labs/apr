import json
from ptri_base import ptri_base

def ptri():
    print("Starting pTRI")

    timestamp = None
    with open('ptri.json') as json_file:
        initial_ptri_data = json.load(json_file)
        timestamp = initial_ptri_data['timestamp']

    data = ptri_base(timestamp)

    with open("ptri.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    ptri()