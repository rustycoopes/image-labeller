from external_api.dbx import RussDropBox
from external_api.gcp_pubsub import ImgPathPubisher
import logging
class ImgPublisher():

    def __init__(self, dropb, publisher = None):
        self._drop_bx = dropb
        self._publisher =  publisher

    def publish_dbx_library(self, dry_run = False):
        """ 
            reads all image locations from dropbox
            Args:
                If dry_run is True the paths are streamed, via yield.
                if dry run is False the paths are published on pubsub, and then yield.
        """
        publish_count = 0
        
        for path in self._drop_bx.get_image_paths():
            
            if not self._should_filter_noise(path):

                publish_count = publish_count + 1
                if not dry_run :#and self._publisher is not None:
                    self._publisher.publish(path)
                
                logging.info('publish {}'.format(path))

                if publish_count % 100 == 0:
                     logging.info('PUBLISHED {} IMAGES'.format(publish_count))

                yield path
                
        
    def _should_filter_noise(self, path):
        # ignore thumbnails.
        return 'nail' in path 