"""
This file is used for Google Cloud functions to collect fees
"""

import base64
from gcc_utils import get_event_id
from ptri_fees_base import ptri_fees_base
import time

TAG = "[GCC_PTRI_FEES] "

def gcc_ptri_fees(event, context):
    event_id = get_event_id(context)

    print(TAG + "Beginning Google Cloud Fn processing of tri fee collection for event_id: {0}".format(event_id))
    
    print(TAG + 'Starting at ' + getTime())

    if 'data' in event:
        try:
            frequency = int(base64.b64decode(event['data']).decode('utf-8'))
            print(TAG, "decoded frequency to " + frequency)
        except:
            print(TAG, "failed to decode frequency ", event['data'])
            print(TAG, "using fallback frequency of 24")
            frequency = 24
    else:
        print(TAG, "'data' not in event; using fallback frequency of 24")
        frequency = 24


    ptri_fees_base(frequency)

    print(TAG + 'Completed at ' + getTime())

def getTime():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time

if __name__ == "__main__":
    gcc_ptri_fees(None, None)
