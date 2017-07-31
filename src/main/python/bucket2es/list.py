#!/usr/bin/env python
# -*- coding: utf-8 -*-
from exceptions import Exception

import boto3
import json
import sys
from auth import *

es_client = init_elasticsearch(init_auth(), sys.argv[3])

print("Looking for '%s' in '%s'" % (sys.argv[2], sys.argv[1]))

try:
    res = es_client.search(index="people_index", doc_type="people", body={"query": {"match": {sys.argv[1]: sys.argv[2]}}})
    print("%d documents found" % res['hits']['total'])
    if res['hits']['total'] == 0:
        exit(2)

    for doc in res['hits']['hits']:
        print(json.dumps(doc['_source']))

    exit(0)

except Exception as e:
    # print(e)
    print("0 documents found")
    exit(1)
