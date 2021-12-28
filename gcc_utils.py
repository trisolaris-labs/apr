"""
General utility methods for interacting with Google Cloud Compute
"""

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
