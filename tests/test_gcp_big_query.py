from google.cloud import bigquery
from external_api.gcp_biquery import BQWriter
import pytest
from mock import patch, Mock

TESTDATASET_NAME = "tds"
TESTTABLE_NAME = "ttn"

@patch('external_api.gcp_biquery.bigquery.Client')
def test_delete_sql_statement_executes(mock_bq_client):
    bq = BQWriter(TESTDATASET_NAME, TESTTABLE_NAME)

    mock_bq_client_instance = mock_bq_client.return_value
    bq.delete_image_data('test_image')

    expectedSql = "DELETE FROM {}.{} WHERE imagepath = '{}'".format(TESTDATASET_NAME, TESTTABLE_NAME, 'test_image')
    mock_bq_client_instance.query.assert_called_with(expectedSql)


@patch('external_api.gcp_biquery.bigquery.Client')
@pytest.mark.parametrize("rows_found, expected_result",
     [(1,True),
    (0,False),
    (40,True),
    (-4,False)])
def test_image_data_exists(mock_bq_client, rows_found, expected_result):
    bq = BQWriter(TESTDATASET_NAME, TESTTABLE_NAME)
    queryJobMock = Mock()
    queryJobMock.result.return_value.total_rows = rows_found
    
    mock_bq_client_instance = mock_bq_client.return_value
    mock_bq_client_instance.query.return_value = queryJobMock
    
    exists = bq.image_data_exists('test_image')

    assert exists == expected_result
    expectedSql = "SELECT * FROM {}.{} WHERE imagepath = '{}'".format(TESTDATASET_NAME, TESTTABLE_NAME, 'test_image')
    mock_bq_client_instance.query.assert_called_with(expectedSql)





