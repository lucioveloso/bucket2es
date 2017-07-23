#!/usr/bin/env bash

trap ctrl_c INT

function ctrl_c() {
        echo "Stopping the generator"
        exit 0
}

source "$(dirname "$0")/../project.conf"

bucket=$(aws cloudformation describe-stack-resources --stack-name $stackname --query 'StackResources[?LogicalResourceId==`myBucket`].PhysicalResourceId' --out text)

while [ true ];
do
    name=$(base64 /dev/urandom | tr -dc 'a-zA-Z' | head -c 15)
    age=$((1 + RANDOM % 100))
    payload="{ \"name\": \"$name\", \"age\": $age }"
    echo -n "$payload" | aws s3 cp - s3://$bucket/auto_generated/$name.json
    echo $payload
done