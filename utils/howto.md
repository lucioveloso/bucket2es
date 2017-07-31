```console
[bucket2es]$ ./setup.sh temporary-bucket
Uploading to tmp/b09dec7fa3e67ebac33be3569e15cda9  882757 / 882757.0  (100.00%)
Successfully packaged artifacts and wrote output template to file packaged-stack.yaml.
Execute the following command to deploy the packaged template
aws cloudformation deploy --template-file /Users/glucio/lambda-toolkit/lambdas/eu-west-1/bucket2es/packaged-stack.yaml --stack-name <YOUR STACK NAME>
aws cloudformation deploy... ./setup.sh is already executing it =)
Waiting for changeset to be created..
Waiting for stack create/update to complete
Successfully created/updated stack - bucket2es

Your bucket name is bucket-bucket2es-432811670411-eu-west-1
You ElasticSearch endpoint is: search-domain-bucket2es-42gx6qn47sn6td2o3uynbnyoca.eu-west-1.es.amazonaws.com
* Please remember that you need authentication to connect to the endpoint.
[bucket2es]$ 
[bucket2es]$ 
[bucket2es]$ utils/upload.sh utils/examples/event1.json
upload: utils/examples/event1.json to s3://bucket-bucket2es-123456789123-eu-west-1/event1.json
[bucket2es]$ utils/upload.sh utils/examples/event2.json
upload: utils/examples/event2.json to s3://bucket-bucket2es-123456789123-eu-west-1/event2.json
[bucket2es]$ utils/upload.sh utils/examples/event3.json
upload: utils/examples/event3.json to s3://bucket-bucket2es-123456789123-eu-west-1/event3.json
[bucket2es]$ 
[bucket2es]$ 
[bucket2es]$ aws s3 ls s3://bucket-bucket2es-123456789123-eu-west-1
2017-07-20 20:43:47         34 event1.json.indexed
2017-07-20 20:43:50         34 event2.json.failed
2017-07-20 20:43:59         44 event3.json.failed
[bucket2es]$ 
[bucket2es]$ utils/search.sh name Lisa
Connecting to search-domain-bucket2es-42gx6qn47sn6td2o3uynbnyoca.eu-west-1.es.amazonaws.com.
Looking for 'Lisa' in 'name'
1 documents found
{"age": 15, "name": "Lisa"}
[bucket2es]$ 
[bucket2es]$ utils/search.sh age 11  
Connecting to search-domain-bucket2es-42gx6qn47sn6td2o3uynbnyoca.eu-west-1.es.amazonaws.com.
Looking for '11' in 'age'
0 documents found
[bucket2es]$ 
[bucket2es]$ utils/upload.sh utils/examples/event2-fixed.json
[bucket2es]$     
[bucket2es]$ utils/search.sh age 11                          
Connecting to search-domain-bucket2es-42gx6qn47sn6td2o3uynbnyoca.eu-west-1.es.amazonaws.com.
Looking for '11' in 'age'
1 documents found
{"age": 11, "name": "Peter"}
[bucket2es]$
[bucket2es]$
[bucket2es]$ utils/autogenerate.sh 
{ "name": "fSajfWQWGtQUIlX", "age": 76 }
{ "name": "hmyVJfGfhhizjmR", "age": 7 }
{ "name": "dbvEcnqEEfANwFJ", "age": 89 }
{ "name": "EaaAgahoqoQBkPO", "age": 28 }
{ "name": "yPsjQcbmfYtQTaR", "age": 55 }
{ "name": "SXtMxWJoYzEWban", "age": 22 }
{ "name": "iRaWApYDymzWTfJ", "age": 19 }
{ "name": "nWlhBqdaQRrsgAQ", "age": 43 }
{ "name": "OfWdoxahwjjxClt", "age": 27 }
^Ccancelled: ctrl-c received
Closing generator
[bucket2es]$
[bucket2es]$
[bucket2es]$ utils/search.sh age 27
Connecting to search-domain-bucket2es-42gx6qn47sn6td2o3uynbnyoca.eu-west-1.es.amazonaws.com.
Looking for '27' in 'age'
1 documents found
{"age": 27, "name": "OfWdoxahwjjxClt"}
[bucket2es]$
[bucket2es]$
[bucket2es]$ utils/search.sh name EaaAgahoqoQBkPO
Connecting to search-domain-bucket2es-42gx6qn47sn6td2o3uynbnyoca.eu-west-1.es.amazonaws.com.
Looking for 'EaaAgahoqoQBkPO' in 'name'
1 documents found
{"age": 28, "name": "EaaAgahoqoQBkPO"}
```