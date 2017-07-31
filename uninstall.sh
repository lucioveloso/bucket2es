#!/usr/bin/env bash

cd "$(dirname "$0")"

source project.conf

stacks=$(aws cloudformation list-stacks --stack-status-filter --query "StackSummaries[?StackStatus!='DELETE_COMPLETE' && StackName=='$stackname']" --out text | wc -l)

if [ "$stacks" -eq 0 ]; then
    echo "The stack $stackname does not exist."
    exit 1
fi

bucket=$(aws cloudformation describe-stack-resources --stack-name $stackname --query 'StackResources[?LogicalResourceId==`myBucket`].PhysicalResourceId' --out text)

aws s3 rm s3://$bucket --recursive > /dev/null 2>&1

# Removing the stack

aws cloudformation delete-stack --stack-name $stackname > /dev/null

if [ $? -ne 0 ]; then
    echo "An unexpected error deleting the stack =("
    exit 1
else
    echo "The stack is being removed."
fi

echo "Check your CloudFormation events to get more details."

exit 0
