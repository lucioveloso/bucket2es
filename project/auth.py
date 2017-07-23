#!/usr/bin/env python
import sys

sys.path.append("/var/task/libs")

from libs.elasticsearch import Elasticsearch
from libs.elasticsearch import RequestsHttpConnection
from libs.requests_aws4auth import AWS4Auth


def init_elasticsearch(auth, my_endpoint_url):

    """ Create an elasticsearch client instance """

    print("Connecting to " + my_endpoint_url + ".")
    try:
        return Elasticsearch(host=my_endpoint_url,
                             port=443,
                             use_ssl=True,
                             connection_class=RequestsHttpConnection,
                             verify_certs=True,
                             http_auth=auth)
    except Exception as e:
        print("Failed to connect in " + my_endpoint_url + ".")
        # print(e)
        exit(1)


def init_auth(s):

    """ Generate a AWS4Auth based in the boto3 variables """

    try:
        cred = s.get_credentials()
        return AWS4Auth(cred.access_key,
                        cred.secret_key,
                        s.region_name, 'es',
                        session_token=cred.token)
    except Exception as e:
        print(e)
        print("Some exception initiating the aws4auth.")
        exit(1)
