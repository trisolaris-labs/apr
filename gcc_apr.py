"""
This file is used for Google Cloud functions to serve apr calculations
"""

from apr_base import apr_base
from gcc_utils import (get_event_id, upload_object_as_json_to_gcc)

# Output file name
FILE_NAME = "datav2.json"

# Google Cloud Storage
TRISOLARIS_APR_BUCKET = "trisolaris_public"
TRISOLARIS_APR_BUCKET_FILE_PATH = FILE_NAME

# This directory is writable by cloud functions; consumes memory resources provisioned for function
GOOGLE_CLOUD_STORAGE_TEMP_DIRECTORY = "/tmp/"

TAG = "[GCC_APR]"

# Gets apr data from `apr_base`
# Uploads result to gcc file storage
def gcc_apr(data, context):
    event_id = get_event_id(context)

    print(TAG + "Beginning Google Cloud Fn processing of apr for event_id: {0}".format(event_id))
    
    result = apr_base()

    print(TAG + "APR calculation completed")

    upload_object_as_json_to_gcc(
        result,
        gcc_bucket=TRISOLARIS_APR_BUCKET,
        gcc_file_path=TRISOLARIS_APR_BUCKET_FILE_PATH,
        make_public=True,
    )

    print(TAG + "Complete Google Cloud Fn processing of apr for event_id: {0}".format(event_id))

if __name__ == "__main__":
    gcc_apr(None, None)
