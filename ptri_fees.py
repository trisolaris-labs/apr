import json
from ptri_fees_base import ptri_fees_base

default_frequency = 24


def ptri_fees():
    print("Starting pTRI fees")

    ptri_fees_base(default_frequency)


if __name__ == "__main__":
    ptri_fees()
