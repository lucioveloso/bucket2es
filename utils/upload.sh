#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "Please execute: $0 <file path>, example:"
    echo "$0 records/event1.json"
    exit 1
fi

source "$(dirname "$0")/../project.conf"

bucket=$(aws cloudformation describe-stack-resources --stack-name $stackname --query 'StackResources[?LogicalResourceId==`myBucket`].PhysicalResourceId' --out text)

aws s3 cp "$1" s3://$bucket
exit $?