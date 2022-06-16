import json
import time
from gcc_utils import get_google_cloud_storage_blob
from xtri_base import xtri_base

TAG = "[GCC_XTRI] "

# Output file name
FILE_NAME = "xtri.json"

# Google Cloud Storage
TRISOLARIS_XTRI_BUCKET = "trisolaris_public"
TRISOLARIS_XTRI_BUCKET_FILE_PATH = FILE_NAME


def gcc_xtri(data, context):
    print(TAG + "Starting at " + getTime())
    blob = get_google_cloud_storage_blob(TRISOLARIS_XTRI_BUCKET, TRISOLARIS_XTRI_BUCKET_FILE_PATH)
    xtri_data = json.loads(blob.download_as_string(client=None))

    result = xtri_base(xtri_data["timestamp"])

    blob.upload_from_string(
        data=json.dumps(result, ensure_ascii=False, indent=4),
        content_type="application/json",
    )

    # Don't serve stale data
    blob.cache_control = "no-cache"

    # Allows file to be publicly accessible
    blob.make_public()

    # Save
    blob.patch()

    print(TAG + "Completed at " + getTime())


def getTime():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time


if __name__ == "__main__":
    gcc_xtri(None, None)
