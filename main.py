""" cloud function entry points for multple triggers (pubsub and http) """

import sys
# [START functions_helloworld_http]
# [START functions_http_content]
from flask import escape

import base64
# [END functions_helloworld_http]
# [END functions_http_content]

import external_api.gcp_biquery


# [START functions_helloworld_pubsub]
def image_labeller_process_subscriber(request):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.

         {'message': {'attributes': {'name': 'russ'}, 'messageId': '1966501043458965', 
         'message_id': '1966501043458965', 'publishTime': '2021-01-31T19:04:14.498Z', 
         'publish_time': '2021-01-31T19:04:14.498Z'}, 
         'subscription': 'projects/rustyware-dev/subscriptions/image-labeller-input-subscription'}
    """
    request_json = request.get_json(silent=True)
    print(request_json)
    if request_json and 'message' in request_json:
        fileName =  base64.b64decode(request_json['message']['data']).decode('utf-8')
        db = external_api.gcp_biquery.BQWriter('image_labels', 'labels')
        db.write_image_data(fileName, '')
    return 'Writing {}!'.format(escape(fileName))
# [END functions_helloworld_pubsub]


