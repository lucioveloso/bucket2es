#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import boto3
sys.path.append("/var/task/libs")

from libs.elasticsearch import Elasticsearch
from libs.elasticsearch import RequestsHttpConnection
from libs.requests_aws4auth import AWS4Auth



def init_elasticsearch(auth, my_endpoint_url):

    """ Create an elasticsearch client instance """

    print("Connecting to " + my_endpoint_url + ".")
    try:
        es = Elasticsearch(host=my_endpoint_url,
                           port=443,
                           use_ssl=True,
                           connection_class=RequestsHttpConnection,
                           verify_certs=True,
                           http_auth=auth)
        es.info()
    except Exception as e:
        raise Exception("Failed to connect in " + my_endpoint_url + ".")
        # print(e)

    return es


def init_auth():

    """ Generate a AWS4Auth based in the boto3 variables """
    session = boto3.session.Session()

    try:
        return AWS4Auth(session.get_credentials().access_key,
                        session.get_credentials().secret_key,
                        session.region_name, 'es',
                        session_token=session.get_credentials().token)
    except Exception as e:
        print(e)
        print("Some exception initiating the aws4auth.")
        exit(1)
