#!/usr/bin/env bash

if [ $# -ne 1 ]; then
    echo "Please execute: $0 <file path>"
    echo "Example:"
    echo "     $0 records/event1.json"
    exit 1
elif [ ! -f $1 ]; then
    echo "$1 is not a file"
    exit 1
fi

source "$(dirname "$0")/../project.conf"

bucket=$(aws cloudformation describe-stack-resources --stack-name $stackname --query 'StackResources[?LogicalResourceId==`myBucket`].PhysicalResourceId' --out text)

if [ $? -ne 0 ]; then
    echo "The $stackname does not exist."
    echo "Please run the setup first"
    exit 1
fi

aws s3 cp "$1" s3://$bucket
exit $?
