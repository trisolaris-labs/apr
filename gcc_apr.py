"""
This file is used for Google Cloud functions to serve apr calculations
"""

import os
import json

from apr_base import apr_base
from google.cloud import storage
from random import randrange

# Output file name
FILE_NAME = "datav2.json"

# Google Cloud Storage
TRISOLARIS_APR_BUCKET = "trisolaris-apr"
TRISOLARIS_APR_BUCKET_FILE_PATH = "apr/" + FILE_NAME

# This directory is writable by cloud functions; consumes memory resources provisioned for function
GOOGLE_CLOUD_STORAGE_TEMP_DIRECTORY = "/tmp/"

TAG = "[GCC_APR]"

# Gets apr data from `apr_base`
# Saves to gcc writeable directory `/tmp/`
# Uploads file from `/tmp/` to gcc cloud storage
# Deletes `/tmp/` file
def gcc_apr(data, context):
    event_id = get_event_id(context)

    print(TAG + "Beginning Google Cloud Fn processing of apr for event_id: {0}".format(event_id))
    
    result = apr_base()

    print(TAG + "APR calculation completed")
    
    temp_file_path = create_temp_path(event_id)
    
    # save output to gcc tmp path
    write_to_path(result, temp_file_path)
    
    # upload file from tmp path to gcc cloud storage
    upload_to_gcc(temp_file_path)

    # delete temp data
    delete_from_tmp(temp_file_path)

# Assigns a random int as event_id if no context is passed 
# eg: running from shell
def get_event_id(context):
    if hasattr(context, 'event_id'):
        return context.event_id
    else:
        return randrange(10e12)

# Creates file path for the specific event_id
# EG: if events processing takes long, an older job could delete newer data
# outputs /tmp/{...eventid...}-datav2.json
def create_temp_path(event_id):
    return "{0}{1}-{2}".format(
        GOOGLE_CLOUD_STORAGE_TEMP_DIRECTORY, 
        event_id,
        FILE_NAME,
    )

# save data to local gcc tmp path
def write_to_path(data, path):
    print(TAG + "Writing apr data to temp path: " + path)
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# uploads file to gcc cloud storage
# sets file as public for allUser access
def upload_to_gcc(path):
    print(TAG + "Uploading to gcc location: {0}{1}".format(TRISOLARIS_APR_BUCKET, TRISOLARIS_APR_BUCKET_FILE_PATH))
    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(TRISOLARIS_APR_BUCKET)
    blob = bucket.get_blob(TRISOLARIS_APR_BUCKET_FILE_PATH)
    blob.upload_from_filename(path)
    blob.make_public()
    
    print(TAG + "Uploading to gcc location: {0}{1} complete".format(TRISOLARIS_APR_BUCKET, TRISOLARIS_APR_BUCKET_FILE_PATH))

# deletes tmp file to free up fn memory
def delete_from_tmp(path):
    try:
        os.remove(path)
        
        print(TAG + "Deleted temporary file at {0}".format(path))
    except OSError:
        pass

if __name__ == "__main__":
    gcc_apr(None, None)
