import json

from apr_base import apr_base


def apr():
    print("Starting APR")
    data = apr_base()

    with open("datav2.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    apr()
