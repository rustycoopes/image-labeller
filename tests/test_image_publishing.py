import pytest
from mock import patch, Mock
from processing.image_publishing import ImgPublisher
from external_api.dbx import RussDropBox
from external_api.gcp_pubsub import ImgPathPubisher

@pytest.fixture
def publisher():
    yield ImgPublisher( RussDropBox('',True, 100), None)


def test_should_skip_thumbnail(mocker):
    
    publisher =  ImgPublisher( RussDropBox('',True, 100), None)
    mocker.patch('processing.image_publishing.RussDropBox.get_image_paths', return_value = ['my_thumb_nail'])
    paths = list(publisher.publish_dbx_library())
   
    assert len(paths) == 0
 
def test_should_return_non_thumbnails(mocker):
    
    publisher =  ImgPublisher( RussDropBox('',True, 100), None)
    mocker.patch('processing.image_publishing.RussDropBox.get_image_paths', return_value = ['my_thumb_nal'])
    paths = list(publisher.publish_dbx_library(True))
   
    assert len(paths) == 1
 
@patch.object(RussDropBox, 'get_image_paths')
def test_should_skip_thumbnail(mock_my_method, publisher):
    
    mock_my_method.return_value = ['my_thumb_nail']
    paths = list(publisher.publish_dbx_library())
   
    assert len(paths) == 0

@patch.object(RussDropBox, 'get_image_paths')
@pytest.mark.parametrize("filenames, return_count",
     [(["'my_thumb_nail"],0),
    (["'my_thumb_nal"],1),
    (["'my_thumb_nal", "nal2"],2)])
def test_should_skip_thumbnails_but_run_others(mock_my_method, publisher, filenames, return_count):   
    mock_my_method.return_value = filenames
    paths = list(publisher.publish_dbx_library(True))
    assert len(paths) == return_count


@patch('external_api.gcp_pubsub.ImgPathPubisher')
@patch('external_api.dbx.RussDropBox')
@pytest.mark.parametrize("filenames",
   [["'my_thumb_nal"], ["'my_thumb_nal2", "nal2"]])
def test_should_skip_thumbnails_but_run_others2(mock_dropbox, mock_messaging, filenames):
    
    dbx_mock = mock_dropbox.return_value
    dbx_mock.get_image_paths.return_value =  filenames
    pub_mock = mock_messaging.return_value

    my_publisher = ImgPublisher( dbx_mock, pub_mock)
    # important to wrap in list, so the yield is exercised
    list(my_publisher.publish_dbx_library(False))
    
    assert pub_mock.publish.call_count == len(filenames)

