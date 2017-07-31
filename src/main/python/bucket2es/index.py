#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import sys
import boto3
import auth

sys.path.append("/var/task/libs")


s3 = boto3.resource('s3')

doc_type = "people"
index_name = "people_index"
index_body = {
    "mappings": {
        "people": {
            "dynamic": 'strict',
            "properties": {
                "name": {
                    "type": "text"
                },
                "age":  {
                    "type": "integer"
                }
            }
        }
    }
}

def init_index(es_client):

    """ Create the index if does not exist """

    if es_client.indices.exists(index_name) is False:
        try:
            es_client.indices.create(index_name, body=index_body)
            print("Created.")
        except Exception as e:
            print(e)
            exit(1)

def es_index_file(es_client, body):

    """ Index the file in the elasticsearch"""

    try:
        es_client.index(index=index_name, doc_type=doc_type, body=body)
        return True
    except Exception as e:
        # print(e)
        print("Some exception indexing the file.")

    return False

def validate_json(json_str):

    """ Validate if the input string is a valid json with the correct attributes / values
    As the json file is too simple, I'm not using an external library to validate the schema. """
    try:
        j = json.loads(json_str)
    except Exception as e:
        return False

    if j is not None and len(j) == 2:
        if 'name' in j and 'age' in j:
            if (type(j['name']) == str or type(j['name']) == unicode) and type(j['age']) == int:
                return True

    return False


def change_processed_file(obj, success):

    """ Change the processed file according with the configured action """

    if os.environ['lambda_action_on_process'] == "rename":
        if success:
            append_ext = ".indexed"
        else:
            append_ext = ".failed"

        s3.Object(obj.bucket_name, obj.key + append_ext).copy_from(CopySource=obj.bucket_name + "/" + obj.key)
        s3.Object(obj.bucket_name, obj.key).delete()
        return "Renamed"
    elif os.environ['lambda_action_on_process'] == "delete":
        s3.Object(obj.bucket_name, obj.key).delete()
        return "Deleted"
    else:
        return "None"

def read_bucket_file(obj):
    try:
        return obj.get()['Body'].read().decode('utf-8')
    except Exception as e:
        #print(e)
        raise ValueError('File does not exist')

def lambda_handler(event, context):

    """ Main lambda function triggered by S3 Notification """

    # Get the endpoint from lambda environment variable
    if 'my_endpoint_url' not in os.environ or 'lambda_action_on_process' not in os.environ:
        raise ValueError('Missing variables')

    # Init aws4auth and elasticsearch
    es_client = auth.init_elasticsearch(auth.init_auth(), os.environ['my_endpoint_url'])

    # Create a index if it does not exist
    init_index(es_client)

    # Read all records in the event (Notification send an array)
    # Probably S3 groups the records in large input event (Need to check)
    if event is None or 'Records' not in event:
        raise ValueError('Invalid event')

    for r in event['Records']:
        try:
            obj_name = r['s3']['bucket']['name']
            obj_key = r['s3']['object']['key']
        except Exception as e:
            raise ValueError('Invalid event record')

        obj = s3.Object(obj_name, obj_key)
        obj_str = read_bucket_file(obj)

        if validate_json(obj_str):
            # Indexing the file
            if es_index_file(es_client, obj_str):
                #print("Indexed.")
                change_processed_file(obj, True)
        else:
            change_processed_file(obj, False)
            raise ValueError('Invalid json file input')


    return "end"
