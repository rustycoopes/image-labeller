


#COLUMNS
#imagepath
#label
#confidence

import logging
from google.cloud import bigquery

class BQWriter():

    def __init__(self, dataset, table):

        self._dataset = dataset
        self._table = table
        pass


    def write_image_data(self, image_path, label, confidence):
        client = bigquery.Client()
        dataset_ref = client.dataset(self._dataset)
        table_ref = dataset_ref.table(self._table)
        table = client.get_table(table_ref)

        #TODO CHECK IF EXISTS FOR IMAGE AND LABEL THEN UPDATE
        #errors = client.insert_rows(table, [( image_path ,label,confidence)])

        dml_statement = "INSERT INTO image_labels.labels (imagepath, label, confidence) VALUES ('{}', '{}', {})".format(image_path, label, confidence)
        logging.debug('running big query {}'.format(dml_statement))
        query_job = client.query(dml_statement)  # API request
        try:
            job_result = query_job.result()  # Waits for statement to finish  
        except:
            for e in query_job.errors:
              logging.error('ERROR: {}'.format(e['message']))


    def delete_image_data(self, image_path):           
        client = bigquery.Client()
        dml_statement = "DELETE FROM image_labels.labels WHERE imagepath = '{}'".format(image_path)
        logging.debug('running big query {}'.format(dml_statement))
        query_job = client.query(dml_statement)  # API request
        try:
            query_job.result()  # Waits for statement to finish           
        except:
            for e in query_job.errors:
              logging.error('ERROR: {}'.format(e['message']))

