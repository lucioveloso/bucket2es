#!/usr/bin/env bash

if [ $# -ne 2 ]; then
	echo "Please execute $0 <attribute> <value>"
	echo "Example:"
	echo "      $0 name Lisa"
	echo "      $0 age 12"
	exit 1
fi

cd "$(dirname "$0")"

source ../project.conf

endpoint=$(aws cloudformation describe-stacks --stack-name $stackname --query 'Stacks[0].Outputs[?OutputKey==`ElasticEndpoint`].OutputValue' --out text)

if [ $? -ne 0 ]; then
    echo "The $stackname does not exist."
    echo "Please run the setup first"
    exit 1
fi

if [[ "$endpoint" == "None" ]]; then
    echo "Failed to load endpoint"
    exit 1
fi

python ../src/main/python/bucket2es/list.py "$1" "$2" $endpoint
exit $?
