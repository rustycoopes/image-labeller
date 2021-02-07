from external_api.dbx import RussDropBox
from external_api.gcp_pubsub import ImgPathPubisher
import configparser
import os
import logging
import sys
class ImgProcessor():

    def __init__(self, dropb, publisher ):
        self._drop_bx = dropb
        self._publisher =  publisher
        pass


    def publish_dbx_library(self):

        for path in self._drop_bx.get_image_paths():
            self._publisher.publish(path)
        


def utils_read_dbx_cfg_from_gcs():
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket('application-core-config')
    blob = bucket.blob('core-config.ini')    
    return blob.download_as_string().decode('utf-8')    

if __name__ == "__main__":
    logging.basicConfig( 
    filename='process_pipeline.log',
    level=logging.DEBUG, 
    format='[%(asctime)s]{%(pathname)s:%(lineno)d}%(levelname)s- %(message)s', 
    datefmt='%H:%M:%S'
) 
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    config = configparser.ConfigParser()
    config.read('./config/main.ini')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=config['DEFAULT']['CredentialsFile']
    logging.info('gcp credentials set to be read from file {}'.format(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]))
    config.read_string(utils_read_dbx_cfg_from_gcs())
  
    # Connect to dropbox, find all images and publish to subsub
    publisher = ImgPathPubisher(config['DEFAULT']['ProjectName'], config['DEFAULT']['ProcessEntryTopic'])
    dropb = RussDropBox(config['DROPBOX-SECRETS']['Token'], max_file_count = int(config['DROPBOX']['MaxSize']), batch_size = int(config['DROPBOX']['BatchSize']))
    processor = ImgProcessor(dropb, publisher)
    processor.publish_dbx_library()

    # test write to bigquery
    # import external_api.gcp_biquery
    # db = external_api.gcp_biquery.BQWriter('image_labels', 'labels')
    # db.write_image_data('Russ Test', 'default', 100)
    # db.remove_duplicates()
    # db.delete_image_data('Russ Test')
    


