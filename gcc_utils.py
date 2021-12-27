"""
General utility methods for interacting with Google Cloud Compute
"""

import json

from google.cloud import storage
from random import randrange

# Assigns a random int as event_id if no context is passed 
# eg: running from shell
def get_event_id(context):
    if hasattr(context, 'event_id'):
        return context.event_id
    else:
        return randrange(10e12)

def get_google_cloud_storage_blob(gcc_bucket, gcc_file_path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(gcc_bucket)
    blob = bucket.get_blob(gcc_file_path)

    return blob

# uploads object as JSON to gcc cloud storage
def upload_object_as_json_to_gcc(data, gcc_bucket, gcc_file_path, make_public):
    print("Uploading to gcc location: {0}/{1}".format(gcc_bucket, gcc_file_path))
    
    blob = get_google_cloud_storage_blob(gcc_bucket, gcc_file_path)

    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    
    with blob.open("wt", chunk_size=256 * 1024) as writer:
        writer.write(json_data)
    
    if (make_public):
        blob.make_public()
    
    print("Uploading to gcc location: {0}/{1} complete".format(gcc_bucket, gcc_file_path))

# uploads object as text to gcc cloud storage
def upload_object_as_text_to_gcc(data, gcc_bucket, gcc_file_path, make_public):
    print("Uploading to gcc location: {0}/{1}".format(gcc_bucket, gcc_file_path))
    
    blob = get_google_cloud_storage_blob(gcc_bucket, gcc_file_path)
    
    with blob.open("wt", chunk_size=256 * 1024) as writer:
        writer.write(data)
    
    if (make_public):
        blob.make_public()
    
    print("Uploading to gcc location: {0}/{1} complete".format(gcc_bucket, gcc_file_path))