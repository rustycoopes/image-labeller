import dropbox
import configparser
import pytest


@pytest.fixture
def token():
    config = configparser.ConfigParser()
    config.read("C:\\Users\\russe\\OneDrive\\dev\\credentials\\dropbox.ini")
    return config['DROPBOX-SECRETS']['Token']

def test_connect_to_dbx(token):
    dbx = dropbox.Dropbox(token)
    assert dbx.users_get_current_account()

def test_list_files(token):
    dbx = dropbox.Dropbox(token)

    response = dbx.files_list_folder('' , recursive=True, limit=100,)
    print (response.has_more )
    print (response.cursor )
    for entry in response.entries:
        print(entry.name)

    while response.has_more:
        print("getting more................")
        response = dbx.files_list_folder_continue(response.cursor )
        for entry in response.entries:
            print(entry.path_lower)

    assert True


import os
import io
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="client_cred.json"


def test_download_files(token):
    dbx = dropbox.Dropbox(token)

    response = dbx.files_list_folder('' , recursive=True, limit=100,)
    print (response.has_more )
    print (response.cursor )
    for entry in response.entries:
        print(entry.name)

    while response.has_more:
        print("getting more................")
        response = dbx.files_list_folder_continue(response.cursor )
        for entry in response.entries:
            if entry.path_lower.endswith('.jpg'):
                file = dbx.files_download(entry.path_lower)
                content = file[1].content
                load_image(content)
#https://www.dropbox.com/preview/Camera%20Uploads/2021-01-30%2016.03.24.mp4?role=personal
                return

    assert True


def load_image(content):
    import urllib
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print("results from image analysis {} : {}".format(label.description, label.score))
    