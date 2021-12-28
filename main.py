"""
This file is used by Google Cloud functions
The methods available in this file are callable by gcp cloud functions 
"""

# Cloud Scheduler - Emits event `Topic:projects/trisolaris-ad-hoc/topics/create_datav2.json` every 2 mins
#   URL: https://console.cloud.google.com/cloudpubsub/topic/detail/create_datav2.json?project=trisolaris-ad-hoc
# Cloud Function - Listens for event and runs `gcc_apr`
#   URL: https://console.cloud.google.com/functions/details/us-central1/gcc_apr?project=trisolaris-ad-hoc
# Cloud Storage - `gcc_apr` saves output to publicly reachable URL
#   URL: https://console.cloud.google.com/storage/browser/_details/trisolaris_public/datav2.json;tab=live_object?project=trisolaris-ad-hoc
#   Public URL: https://storage.googleapis.com/trisolaris_public/datav2.json
from gcc_apr import gcc_apr

# Cloud Scheduler - Emits event `Topic:projects/trisolaris-ad-hoc/topics/calculate_circulating_supply` every 5 mins
#   URL: https://console.cloud.google.com/cloudpubsub/topic/detail/calculate_circulating_supply?project=trisolaris-ad-hoc
# Cloud Function - Listens for event and runs `gcc_total_circulating_supply`
#   URL: https://console.cloud.google.com/functions/details/us-central1/gcc_total_circulating_supply?project=trisolaris-ad-hoc
# Cloud Storage - `gcc_total_circulating_supply` saves output to publicly reachable URL
#   URL: https://console.cloud.google.com/storage/browser/_details/trisolaris_public/circulating_supply.txt;tab=live_object?project=trisolaris-ad-hoc
#   Public URL: https://storage.googleapis.com/trisolaris_public/circulating_supply.txt
from gcc_total_circulating_supply import gcc_total_circulating_supply