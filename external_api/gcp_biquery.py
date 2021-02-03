


#COLUMNS
#imagepath
#label
#confidence

import logging
from google.cloud import bigquery
from google.cloud import pubsub

class BQWriter():

    def __init__(self, dataset, table):

        self._dataset = dataset
        self._table = table
        pass


    def write_image_data(self, image_path, label_info):
        client = bigquery.Client()
        dataset_ref = client.dataset(self._dataset)
        table_ref = dataset_ref.table(self._table)
        table = client.get_table(table_ref)

        #TODO CHECK IF EXISTS FOR IMAGE AND LABEL THEN UPDATE
        errors = client.insert_rows(table, [('imagepath', image_path), ('label', 'default'), ('confidence',100)])
        if not errors:
            logging.info('Saved {} into {}:{}'.format(image_path, self._dataset, self._table))
        else:
            print('Errors:')
            for error in errors:
                 logging.error(error)
