""" cloud function entry points for multple triggers (pubsub and http) """

from flask import escape
import base64
import external_api.gcp_biquery
import external_api.dbx
import configparser

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
    #print(request_json)
    if request_json and 'message' in request_json:
        fileName =  base64.b64decode(request_json['message']['data']).decode('utf-8')
        store = ImgLabelPersitance()
        if store.image_data_exists(fileName):
            return 'data already processed'

        config = configparser.ConfigParser()
        config.read('./config/main.ini')
        config.read_string(utils_read_dbx_cfg_from_gcs())
        dropb = external_api.dbx.RussDropBox(config['DROPBOX-SECRETS']['Token'], max_file_count = int(config['DROPBOX']['MaxSize']), batch_size = int(config['DROPBOX']['BatchSize']))
        
        image = dropb.get_image(fileName)
        labels = get_labels(image)
        if labels is None:
            print('no labels for image')
            return 'ok - no labels'

        for label in labels:
            print("results for {} from image analysis {} : {}".format(fileName, label.description, label.score))
            store.persist(fileName, label.description, label.score)
    
    return 'ok added'

def image_labeller_merge_data(request):
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
    print('merging data to remove duplicates')
    config = configparser.ConfigParser()
    config.read('./config/main.ini')
    store = ImgLabelPersitance()
    store.remove_duplicates()
    return 'Ok de-duped'


def utils_read_dbx_cfg_from_gcs():
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket('application-core-config')
    blob = bucket.blob('core-config.ini')    
    return blob.download_as_string().decode('utf-8')    

def get_labels(content):
    import urllib
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return labels
    

class ImgLabelPersitance():
    def persist(self, fileName, label, confidence):
        db = external_api.gcp_biquery.BQWriter('image_labels', 'labels')
        db.write_image_data(fileName, label, confidence)

# [END functions_helloworld_pubsub]


