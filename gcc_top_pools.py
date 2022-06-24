"""
This file is used for Google Cloud functions to update the top pools in the last 24 hours
"""

import json

from top_pools_base import top_pools_base
from gcc_utils import (gccPrint, get_event_id, get_google_cloud_storage_blob)

# Output file name
FILE_NAME = "pools.json"

# Google Cloud Storage
TRISOLARIS_BUCKET = "trisolaris_public"
TRISOLARIS_BUCKET_FILE_PATH = FILE_NAME

TAG = "[GCC_TOP_POOLS]"

# Gets fee data from covalent api
# Uploads result to gcc file storage
def gcc_top_pools(data, context):
    event_id = get_event_id(context)

    gccPrint(TAG + "Beginning Google Cloud Fn processing of top pools for event_id: {0}".format(event_id))
    
    result = top_pools_base()

    if len(result) == 0:
        gccPrint(TAG + f"Received 0 items, not uploading to GCC")
        return
    
    gccPrint(TAG + f"fetched {len(result)} pools with 24h volume > $100")

    blob = get_google_cloud_storage_blob(TRISOLARIS_BUCKET, TRISOLARIS_BUCKET_FILE_PATH)

    json_data = json.dumps(result, ensure_ascii=False, indent=4)

    blob.upload_from_string(json_data, "application/json")

    # Don't serve stale data
    blob.cache_control = 'no-cache'
    
    # Allows file to be publicly accessible
    blob.make_public()

    # Save
    blob.patch()
    
    gccPrint(TAG + "Uploading to gcc location: {0}/{1} complete".format(TRISOLARIS_BUCKET, TRISOLARIS_BUCKET_FILE_PATH))

if __name__ == "__main__":
    gcc_top_pools(None, None)
