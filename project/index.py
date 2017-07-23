#!/usr/bin/env python

import os
import sys
import boto3
import json
from auth import *

sys.path.append("/var/task/libs")

# Get the endpoint from lambda environment variable
my_endpoint_url = os.environ['my_endpoint_url']
lambda_action_on_process = os.environ['lambda_action_on_process']

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
        if len(j) == 2:
            if 'name' in j and 'age' in j:
                if type(j['name']) == str and type(j['age']) == int:
                    return True
    except Exception as e:
        # print(e)
        pass

    return False

def change_processed_file(obj, success):

    """ Change the processed file according with the configured action """

    if lambda_action_on_process == "rename":
        if success:
            append_ext = ".indexed"
        else:
            append_ext = ".failed"

        s3.Object(obj.bucket_name, obj.key + append_ext).copy_from(CopySource=obj.bucket_name + "/" + obj.key)
        s3.Object(obj.bucket_name, obj.key).delete()
        print("Renamed.")
    elif lambda_action_on_process == "delete":
        s3.Object(obj.bucket_name, obj.key).delete()
        print("Deleted")
    else:
        print("No action")


def lambda_handler(event, context):

    """ Main lambda function triggered by S3 Notification """

    # Init aws4auth and elasticsearch
    es_client = init_elasticsearch(init_auth(boto3.session.Session()), my_endpoint_url)

    # Create a index if it does not exist
    init_index(es_client)

    # Read all records in the event (Notification send an array)
    # Probably S3 groups the records in large input event (Need to check)
    for r in event['Records']:
        obj_name = r['s3']['bucket']['name']
        obj_key = r['s3']['object']['key']
        obj = s3.Object(obj_name, obj_key)
        obj_str = obj.get()['Body'].read().decode('utf-8')
        if validate_json(obj_str):
            # Indexing the file
            if es_index_file(es_client, obj_str):
                print("Indexed.")
                change_processed_file(obj, True)
        else:
            print("Invalid input. Skipping index.")
            change_processed_file(obj, False)
            print(obj_str)

    return "end"
