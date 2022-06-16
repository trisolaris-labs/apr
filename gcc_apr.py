"""
This file is used for Google Cloud functions to serve apr calculations
"""

import json

from apr_base import apr_base
from gcc_utils import get_event_id, get_google_cloud_storage_blob

# Output file name
FILE_NAME = "datav2.json"

# Google Cloud Storage
TRISOLARIS_APR_BUCKET = "trisolaris_public"
TRISOLARIS_APR_BUCKET_FILE_PATH = FILE_NAME

TAG = "[GCC_APR]"


# Gets apr data from `apr_base`
# Uploads result to gcc file storage
def gcc_apr(data, context):

    event_id = get_event_id(context)

    print(
        TAG
        + "Beginning Google Cloud Fn processing of apr for event_id: {0}".format(
            event_id
        )
    )

    result = apr_base()

    print(TAG + "APR calculation completed")

    blob = get_google_cloud_storage_blob(
        TRISOLARIS_APR_BUCKET, TRISOLARIS_APR_BUCKET_FILE_PATH
    )

    json_data = json.dumps(result, ensure_ascii=False, indent=4)

    blob.upload_from_string(json_data, "application/json")

    # Don't serve stale data
    blob.cache_control = "no-cache"

    # Allows file to be publicly accessible
    blob.make_public()

    # Save
    blob.patch()

    print(
        TAG
        + "Uploading to gcc location: {0}/{1} complete".format(
            TRISOLARIS_APR_BUCKET, TRISOLARIS_APR_BUCKET_FILE_PATH
        )
    )


if __name__ == "__main__":
    gcc_apr(None, None)
