"""
This file is used for Google Cloud functions to distribute fees to pTRI holders and calculate APR
"""

from gcc_utils import get_event_id
from ptri_base import ptri_base
import json
import time
from gcc_utils import get_google_cloud_storage_blob, gccPrint

TAG = "[GCC_PTRI] "

# Output file name
FILE_NAME = "ptri.json"

# Google Cloud Storage
TRISOLARIS_BUCKET = "trisolaris_public"
TRISOLARIS_BUCKET_FILE_PATH = FILE_NAME
# Uploads result to gcc file storage
def gcc_ptri(data, context):
    event_id = get_event_id(context)

    gccPrint(
        TAG
        + "Beginning Google Cloud Fn processing of pTRI reward distribution for event_id: {0}".format(
            event_id
        )
    )

    gccPrint(TAG + "Starting at " + getTime())
    blob = get_google_cloud_storage_blob(TRISOLARIS_BUCKET, TRISOLARIS_BUCKET_FILE_PATH)
    ptri_data = json.loads(blob.download_as_string(client=None))

    result = ptri_base(ptri_data[-1]["timestamp"])
    ptri_data.append(result)

    data_to_be_uploaded = []
    if len(data) < 7:
        data_to_be_uploaded = ptri_data
    else:
        data_to_be_uploaded = ptri_data[-7:]

    blob.upload_from_string(
            data=json.dumps(data_to_be_uploaded, ensure_ascii=False, indent=4),
            content_type="application/json",
    )
    
    # Don't serve stale data
    blob.cache_control = "no-cache"

    # Allows file to be publicly accessible
    blob.make_public()

    # Save
    blob.patch()

    gccPrint(TAG + "Completed at " + getTime())

    gccPrint(TAG + "Reward distribution completed")


def getTime():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time


if __name__ == "__main__":
    gcc_ptri(None, None)
