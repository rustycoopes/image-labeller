


#COLUMNS
#imagepath
#label
#confidence

import logging
from google.cloud import bigquery
from datetime import datetime


 
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

        errors = client.insert_rows(table, [( image_path ,label,confidence, None )])

        if errors == []:
            logging.debug("New rows have been added")
        else:
            logging.debug("Encountered errors while inserting rows: {}".format(errors))

    def image_data_exists(self, imagepath):
        client = bigquery.Client()
        bigquery.QueryJob
        query_job = client.query(
            """SELECT * FROM {}.{} WHERE imagepath = '{}'""".format(self._dataset, self._table, imagepath)
        )

        results = query_job.result()  # Waits for job to complete.

        if results is not None and results.total_rows > 0:
            logging.debug('found {} rows for file {}'.format(results.total_rows, imagepath))
            return True
        else:
            return False

    def remove_duplicates(self):
        client = bigquery.Client()
        
        dml_statement = 'CREATE OR REPLACE TABLE {}.{} AS SELECT DISTINCT * FROM {}.{}};'.format(self._dataset, self._table,self._dataset, self._table)  
        query_job = client.query(dml_statement)  # API request
        try:
            query_job.result()  # Waits for statement to finish           
        except:
            for e in query_job.errors:
              logging.error('ERROR: {}'.format(e['message']))
        pass

        # DML insert, reaches max connections when inserting > 20 at any one time 
        # dml_statement = "INSERT INTO image_labels.labels (imagepath, label, confidence) VALUES ('{}', '{}', {})".format(image_path, label, confidence)
        # logging.debug('running big query {}'.format(dml_statement))
        # query_job = client.query(dml_statement)  # API request
        # try:
        #     job_result = query_job.result()  # Waits for statement to finish  
        # except:
        #     for e in query_job.errors:
        #       logging.error('ERROR: {}'.format(e['message']))


    def delete_image_data(self, image_path):           
        client = bigquery.Client()
        dml_statement = "DELETE FROM {}.{} WHERE imagepath = '{}'".format(self._dataset, self._table,image_path)
        logging.debug('running big query {}'.format(dml_statement))
        query_job = client.query(dml_statement)  # API request
        try:
            query_job.result()  # Waits for statement to finish           
        except:
            for e in query_job.errors:
              logging.error('ERROR: {}'.format(e['message']))

