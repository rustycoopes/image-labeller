# image-labeller

This project scans for images within a dropbox location.
The scanned image locations are published to a gcp pubsub topic
A cloud function subscribes to the pubsub topic.
On invocation of the cloud function, the 
  *  image is downloaded
  *  sent to vision api to extract labels
  *  store the labels and image locations in big query  



___
## Architecture
<dl> 
  <dt>image_publisher_app.py</dt>
  <dd>Python app scanns a dropbox location, finds all images and then publishes that image location to a pubsub topic, which is subscribed to by the cloud function</dd>

  <dt>main.py</dt>
  <dd>main.py contains the cloud function itself.  This does the heavy lifting of downloading the file, calling the vision api, and the storing the data.  This will migrate to dataflow.</dd>

  <dt>config</dt>
  <dd>When running locally i use a local credentials file for accessing gcp services.  I store the token for my dropbox account within a gcp bucket (its in a python configparser format).  I have found this most secure.
  Clearly you need to limit access your accounts have to your resources (largely readonly).</dd>

  <dt>Build</dt>
  <dd>I use google cloud build.  I have found im more reliant on this, mainly as the ability to deploy is VERY easy.  I deploy to my cloud function via the build.</dd>

</dl>

___
## Install and setup

[ ] pip install -r requirements.txt
[ ] pytest
[ ] create gcp credentials file
[ ] download your dropbox token
[ ] update date the config to reflect the token locations (/config/main.ini)
