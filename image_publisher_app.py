from external_api.dbx import RussDropBox
from external_api.gcp_pubsub import ImgPathPubisher
from processing.image_publishing import ImgPublisher
from processing.image_labeller_pipeline import ImgLabelPipeLine
from processing.image_labeller_pipeline import ImgLabelPersitanceMock
import configparser
import os
import logging
import sys

def utils_read_dbx_cfg_from_gcs():
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket('application-core-config')
    blob = bucket.blob('core-config.ini')    
    return blob.download_as_string().decode('utf-8')    

def setup_logger():
    logging.basicConfig( 
    filename='process_pipeline.log',
    level=logging.INFO, 
    format='[%(asctime)s]{%(pathname)s:%(lineno)d}%(levelname)s- %(message)s', 
    datefmt='%H:%M:%S'
    ) 
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


if __name__ == "__main__":

    # Setup logger
    setup_logger()
     
    # read app config
    config = configparser.ConfigParser()
    config.read('./config/main.ini')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=config['DEFAULT']['CredentialsFile']
    logging.info('gcp credentials set to be read from file {}'.format(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]))
    config.read_string(utils_read_dbx_cfg_from_gcs())
  
    # Connect to dropbox, find all images and publish to subsub
    publisher = ImgPathPubisher(config['DEFAULT']['ProjectName'], config['DEFAULT']['ProcessEntryTopic'])
    dropb = RussDropBox(config['DROPBOX-SECRETS']['Token'], max_file_count = int(config['DROPBOX']['MaxSize']), batch_size = int(config['DROPBOX']['BatchSize']))
    
    processor = ImgPublisher(dropb, publisher)
    mockStorage  =ImgLabelPersitanceMock('mock','mock')
    lblPipeLine = ImgLabelPipeLine(dropb, mockStorage)

    for path in processor.publish_dbx_library(True):
        lblPipeLine.label(path)

    # test write to bigquery
    # import external_api.gcp_biquery
    # db = external_api.gcp_biquery.BQWriter('image_labels', 'labels')
    # db.write_image_data('russ test', 'default', 100)
    # print(db.image_data_exists('/camera uploads/2012-08-01 17.43.26.jpg'))
    
    # db.remove_duplicates()
    # db.delete_image_data('russ test')



    


