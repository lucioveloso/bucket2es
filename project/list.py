#!/usr/bin/env python

import boto3
import json
import sys
from auth import *


es_client = init_elasticsearch(init_auth(boto3.session.Session()), sys.argv[3])

print("Looking for '%s' in '%s'" % (sys.argv[2], sys.argv[1]))

res = es_client.search(index="people_index", doc_type="people", body={"query": {"match": {sys.argv[1]: sys.argv[2]}}})
print("%d documents found" % res['hits']['total'])
for doc in res['hits']['hits']:
    print(json.dumps(doc['_source']))
