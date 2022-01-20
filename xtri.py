import json
from xtri_base import xtri_base

with open('xtri.json') as json_file:
    xtri_data = json.load(json_file)

result = xtri_base(xtri_data["timestamp"])

with open('xtri.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
