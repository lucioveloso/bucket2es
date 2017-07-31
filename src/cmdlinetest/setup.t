#!/usr/bin/env cram
# vim: set syntax=cram :

##
## Testing setup.sh and uninstall.sh
## (Empty environment)

# General conf
  $ export PROJECTROOTDIR="$TESTDIR/../.." 
  $ cd $PROJECTROOTDIR

# Trying uninstall
  $ ./uninstall.sh
  The * does not exist. (glob)
  [1]

# Trying setup without s3 argument:
  $ ./setup.sh
  A temporary bucket name is required. Please set a bucket in project.conf file or execute * (glob)
  Note that this bucket will be used just to package your lambda during the cloudformation packaging.
  [1]

# Trying extra invalid arguments:
  $ ./setup.sh a b 
  Maximum of 1 argument.
  Execute *setup.sh <temp-bucket> (glob)
  [1]

# Trying setup with non-existing bucket:
  $ ./setup.sh fake-buckets-sdfs-sdfasdsf-asdfsafsa
  
  Unable to upload artifact * referenced by Code parameter of myLambda resource. (glob)
  S3 Bucket does not exist. Execute the command to create a new bucket
  aws s3 mb s3://fake-buckets-sdfs-sdfasdsf-asdfsafsa
  An unexpected error packaging =(
  Did you provide a valid and accessible bucket?
  [1]

# Trying setup using non accessible bucket
  $ ./setup.sh bucket
  
  Unable to upload artifact * referenced by Code parameter of myLambda resource. (glob)
  An error occurred (AccessDenied) when calling the PutObject operation: Access Denied
  An unexpected error packaging =(
  Did you provide a valid and accessible bucket?
  [1]

##
## Testing utils (search.sh, upload.sh)
## (Empty environment)

  $ cd $PROJECTROOTDIR/utils

# Trying to search without arguments / testing help
  $ ./upload.sh
  Please execute: *upload.sh <file path> (glob)
  Example:
      *upload.sh records/event1.json (glob)
  [1]

# Trying to search with only two arguments
  $ ./upload.sh arg1 arg2 > /dev/null 2>&1
  [1]

# Trying to upload a fake file
  $ ./upload.sh fakefile.txt
  * is not a file (glob)
  [1]

# Trying to upload a valid file
  $ ./upload.sh upload.sh
  
  An error occurred (ValidationError) when calling the DescribeStackResources operation: Stack with id * does not exist (glob)
  The * does not exist. (glob)
  Please run the setup first
  [1]

# Trying to search without arguments / testing help Must fail)
  $ ./search.sh
  Please execute *search.sh <attribute> <value> (glob)
  Example:
        *search.sh name Lisa (glob)
        *search.sh age 12 (glob)
  [1]

# Trying to search with only one argument (Must fail)
  $ ./search.sh name > /dev/null 2>&1
  [1]

# Trying to search with only three argument (Must fail)
  $ ./search.sh name fake extraone > /dev/null 2>&1
  [1]

# Trying to search before to create the stack
  $ ./search.sh fakename 12
  
  An error occurred (ValidationError) when calling the DescribeStacks operation: Stack with id * does not exist (glob)
  The * does not exist. (glob)
  Please run the setup first
  [1]

##
## Setting up the environment
##

  $ cd $PROJECTROOTDIR

# Trying to set up using a valid bucket
  $ ./setup.sh lucio-bucket > /dev/null 2>&1

##
## Testing utils scripts
##

  $ cd $PROJECTROOTDIR/utils

# Searching without index
  $ ./search.sh a b
  Connecting to *.es.amazonaws.com. (glob)
  Looking for 'b' in 'a'
  0 documents found
  [1]

# Uploading an event
  $ ./upload.sh examples/event1.json > /dev/null

# Searching with index non existing field
  $ ./search.sh a b
  Connecting to *.es.amazonaws.com. (glob)
  Looking for 'b' in 'a'
  0 documents found
  [2]

# Searching existing name
  $ ./search.sh name Lisa > /dev/null 2>&1

# Search existing age
  $ ./search.sh age 15 > /dev/null 2>&1

# Search non existing age
  $ ./search.sh age 99 > /dev/null 2>&1
  [2]

# Testing uninstall

  $ cd $PROJECTROOTDIR

  $ ./uninstall.sh 
  The stack is being removed.
  Check your CloudFormation events to get more details.
