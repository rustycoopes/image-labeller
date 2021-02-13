import external_api.gcp_biquery
import external_api.dbx
import logging

class ImgLabelPipeLine():
    def __init__(self, dropb, labelStore):
        self._dropb = dropb
        self._lblStore = labelStore
        pass

    def label_image(self, fileName):

        image = self._dropb.get_image(fileName)
        labels = self._get_labels(image)
        
        if labels is None:
            logging.debug('no labels for image')
            return False

        for label in labels:
            logging.debug("results for {} from image analysis {} : {}".format(fileName, label.description, label.score))
            self._lblStore.persist(fileName, label.description, label.score)

        return True

    def _get_labels(self,content):
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        return labels
    

class ImgLabelPersitance():
    def __init__(self, dataset_name, table_name):
        self._dataset_name = dataset_name
        self._table_name = table_name

    def persist(self, fileName, label, confidence):
        db = external_api.gcp_biquery.BQWriter( self._dataset_name,  self._table_name)
#        db = external_api.gcp_biquery.BQWriter('image_labels', 'labels')
        db.write_image_data(fileName, label, confidence)

    def image_data_exists(self, fileName):
        db = external_api.gcp_biquery.BQWriter( self._dataset_name,  self._table_name)
        db.image_data_exists(fileName)

    def remove_duplicates(self):
        db = external_api.gcp_biquery.BQWriter( self._dataset_name,  self._table_name)
        db.remove_duplicates()

class ImgLabelPersitanceMock(ImgLabelPersitance):

    def persist(self, fileName, label, confidence):
        logging.info('Mock persist {} {} {}'.format(fileName, label, confidence))

    def image_data_exists(self, fileName):
        logging.info('Mock looking for data for {} will return true'.format(fileName))
        return True

    def remove_duplicates(self):
        logging.info('Mock remove dups')

