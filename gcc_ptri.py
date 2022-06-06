"""
This file is used for Google Cloud functions to collect fees and distribute them to pTRI holders
"""

from gcc_utils import get_event_id
from ptri_base import ptri_base

TAG = "[GCC_PTRI] "

# Uploads result to gcc file storage
def gcc_ptri(data, context):
    event_id = get_event_id(context)

    print(TAG + "Beginning Google Cloud Fn processing of pTRI reward distribution for event_id: {0}".format(event_id))
    
    ptri_base(None)

    print(TAG + "Reward distribution completed")

if __name__ == "__main__":
    gcc_ptri(None, None)
