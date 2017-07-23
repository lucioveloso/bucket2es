
# Introduction


This project is a Proof of Concept regarding transferring json files from a Bucket to an ElasticSearch. The technologies involved are:

 * S3
 * Lambda
 * ElasticSearch
 * CloudFormation

#### Prerequisites:

* AWS cli configured (credentials / region) and in the system path.
* Bash environment
* Temporary bucket just to be used during the cloudformation packaging. (Full automated deploy)

# Installation


* Cloning the repository

    ```bash
    [~]$ git clone https://github.com/lucioveloso/bucket2es
    ```
    
* Setting up the stack
    
    Note that a temporary bucket name is required to package the stack. The default stack name is bucket2es. You can specify and change those configurations in the file project.conf.
        
    ```bash
   $ cd bucket2es
   [bucket2es]$ ./setup.sh my-temp-bucket
    ```
      
Done! You environment now is created and running.

## Some tools to test the usage:

##### Generating events

* It will just copy the file to the bucket created in the cfn stack

    ```bash
    [bucket2es]$ utils/upload.sh utils/examples/event1.json
    [bucket2es]$ utils/upload.sh utils/examples/event2.json # This one is invalid because it's missing ':' after the age field.
    [bucket2es]$ utils/upload.sh utils/examples/event3.json # This one is invalid because the field age is a string.
     ```
    
#### Searching in the ElasticSearch

* You can search in ElasticSearch using name or age:

     ```bash
     [bucket2es]$ utils/search.sh name Lisa
     Looking for 'Lisa' in 'name'
     1 documents found
     {"age": 15, "name": "Lisa"}
     ```

* Generating random names
    ```bash
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
    Stopping the generator
    [bucket2es]$
    [bucket2es]$
    [bucket2es]$ utils/search.sh age 27
    Connecting to search-domain-bucket2es-42gx6qn47sn6td2o3uynbnyoca.eu-west-1.es.amazonaws.com.
    Looking for '27' in 'age'
    1 documents found
    {"age": 27, "name": "OfWdoxahwjjxClt"}
    ```

* Check all the process in utils/howto.md

#### General Notes:

* This POC assumes that you will handle new files generated in the bucket. In a case of large amount including previous existing files, a solution using **Amazon Kinesis Firehose** is recommended.

* The solution is assuming the input files consists in a json file with ``name`` (type ``string``) and age (type ``int``). A strict index mapping is created with those attributes. There is also a previous checking in the lambda method ``validate_json``.

* Once the lambda process the file, you can determine if the file will be renamed, deleted or kept in the same way. You can set the action configuring ``lambda_action_on_process`` in ``project.conf``. The default action is rename the file.

    * Rename option will append in the file the extension ```.indexed``` if it is valid or ``.failed`` if it is not valid.

* The default stack name is bucket2es, however you can also change it inside the file ``project.conf``

* The cloudformation stack needs to be packaged before to be deployed.  **If you'll deploy using ``setup.sh``, you dont need to concern.** However if you want to deploy without using the script ``./setup.sh`` (using CloudFormation Console, for example), you should add the "Code" properties in the myLambda resource in the ``cfn-stack.yaml``. In this case, you need to manually generate a ``.zip`` from the lambda folder and upload to a temporary bucket.

    ```yaml
   myLambda:
      Properties:
         Code:
             S3Bucket: lucio-bucket
             S3Key: lambda-folder.zip
         Description: ...
         ....
    ```

* To delete the environment, you just need to delete the stack. Make sure that the bucket created is empty before deleting.


#### Diagrams

![Diagram 1](https://github.com/lucioveloso/bucket2es/raw/master/utils/diagrams/diagram1.png)


![Diagram 2](https://github.com/lucioveloso/bucket2es/raw/master/utils/diagrams/diagram2.png)
