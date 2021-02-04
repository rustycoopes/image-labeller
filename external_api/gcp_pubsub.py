from google.cloud import pubsub_v1
import logging

class ImgPathPubisher():
    def __init__(self, project_name, topic_name):
        logging.info('publisher created on project {}, topic {}'.format(project_name, topic_name))
        self._publisher = pubsub_v1.PublisherClient()
        self._topic_path = self._publisher.topic_path(project_name,topic_name)

    def publish(self, image_path):
        logging.debug('publishing message {}'.format(image_path))
        self._publisher.publish(self._topic_path, data=image_path.encode("utf-8"))
        return 'OK', 200
        
