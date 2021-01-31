""" cloud function entry points for multple triggers (pubsub and http) """

import sys
# [START functions_helloworld_http]
# [START functions_http_content]
from flask import escape

# [END functions_helloworld_http]
# [END functions_http_content]



# [START functions_helloworld_get]
def hello_get(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    return 'Hello Rusty World!'
# [END functions_helloworld_get]


# [START functions_helloworld_http]
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(escape(name))
# [END functions_helloworld_http]


# [START functions_helloworld_pubsub]
def image_labeller_process_subscriber(request):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """
    print ("in gunction")
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(escape(name))
# [END functions_helloworld_pubsub]


# [START functions_helloworld_storage]
def hello_gcs(event, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.
    Args:
        event (dict):  The dictionary with data specific to this type of event.
                       The `data` field contains a description of the event in
                       the Cloud Storage `object` format described here:
                       https://cloud.google.com/storage/docs/json_api/v1/objects#resource
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """

    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(event['bucket']))
    print('File: {}'.format(event['name']))
    print('Metageneration: {}'.format(event['metageneration']))
    print('Created: {}'.format(event['timeCreated']))
    print('Updated: {}'.format(event['updated']))
# [END functions_helloworld_storage]


# [START functions_http_content]
def hello_content(request):
    """ Responds to an HTTP request using data from the request body parsed
    according to the "content-type" header.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'name' in request_json:
            name = request_json['name']
        else:
            raise ValueError("JSON is invalid, or missing a 'name' property")
    elif content_type == 'application/octet-stream':
        name = request.data
    elif content_type == 'text/plain':
        name = request.data
    elif content_type == 'application/x-www-form-urlencoded':
        name = request.form.get('name')
    else:
        raise ValueError("Unknown content type: {}".format(content_type))
    return 'Hello {}!'.format(escape(name))
# [END functions_http_content]


# [START functions_http_method]
def hello_method(request):
    """ Responds to a GET request with "Hello world!". Forbids a PUT request.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    from flask import abort

    if request.method == 'GET':
        return 'Hello World!'
    elif request.method == 'PUT':
        return abort(403)
    else:
        return abort(405)
# [END functions_http_method]


def hello_error_1(request):
    # [START functions_helloworld_error]
    # This WILL be reported to Stackdriver Error
    # Reporting, and WILL NOT show up in logs or
    # terminate the function.
    from google.cloud import error_reporting
    client = error_reporting.Client()

    try:
        raise RuntimeError('I failed you')
    except RuntimeError:
        client.report_exception()

    # This WILL be reported to Stackdriver Error Reporting,
    # and WILL terminate the function
    raise RuntimeError('I failed you')

    # [END functions_helloworld_error]


def hello_error_2(request):
    # [START functions_helloworld_error]
    # These errors WILL NOT be reported to Stackdriver
    # Error Reporting, but will show up in logs.
    import logging
    print(RuntimeError('I failed you (print to stdout)'))
    logging.warn(RuntimeError('I failed you (logging.warn)'))
    logging.error(RuntimeError('I failed you (logging.error)'))
    sys.stderr.write('I failed you (sys.stderr.write)\n')

    # This is considered a successful execution and WILL NOT be reported to
    # Stackdriver Error Reporting, but the status code (500) WILL be logged.
    from flask import abort
    return abort(500)
    # [END functions_helloworld_error]