import pytest

from google.cloud import vision
import os
import io
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="client_cred.json"

def test_call_google_Service():
    client = vision.ImageAnnotatorClient()
    path = './tests/test_photo.jpg'
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print("{} : {}".format(label.description, label.score))
    