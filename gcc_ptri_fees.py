"""
This file is used for Google Cloud functions to collect fees
"""

from gcc_utils import gccPrint, get_event_id
from ptri_fees_base import ptri_fees_base
import time

TAG = "[GCC_PTRI_FEES] "

def gcc_ptri_fees(event, context):
    try:
        event_id = get_event_id(context)

        print(TAG + "Beginning Google Cloud Fn processing of tri fee collection for event_id: {0}".format(event_id))
        
        print(TAG + 'Starting at ' + getTime())

        frequency = int(event.get('attributes', {}).get('frequency', 24))
        print(TAG + "Using frequency: ", frequency)

        ptri_fees_base(frequency)

        print(TAG + 'Completed at ' + getTime())
    except Exception as e:
        gccPrint(e, "ERROR")


def getTime():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time

if __name__ == "__main__":
    gcc_ptri_fees(None, None)
