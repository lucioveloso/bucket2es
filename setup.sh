#!/usr/bin/env bash

source project.conf

if [ -n $1 ]; then
    bucket_tmp_name=$1
fi

if [ -z $bucket_tmp_name ]; then
    echo "A temporary bucket name is required. Please set a bucket in project.conf file or execute $0 <temp-bucket>"
    echo "Note that this bucket will be used just to package your lambda during the cloudformation packaging."
    exit 1
fi

###### Setting up the environment ######

cd "$(dirname "$0")"

packaged_tmp_template="packaged-stack.yaml"


# generating the packaged stack
aws cloudformation package \
	--template-file project/cfn-stack.yaml \
	--s3-bucket $bucket_tmp_name \
	--s3-prefix $bucket_tmp_prefix \
	--output-template-file $packaged_tmp_template \


if [ $? -ne 0 ]; then
    echo "An unexpected error packaging =("
    echo "Did you provide a valid and accessible bucket?"
    exit 1
fi

echo "aws cloudformation deploy... $0 is already executing it =)"
echo "========================================================================="
echo "== If it's the first time executing it... keep calm and grab a coffee. =="
echo "========================================================================="
echo

# creating/updating the packaged stack
aws cloudformation deploy \
    --template $packaged_tmp_template \
    --stack-name $stackname \
    --parameter-overrides lambdaActionOnProcess=$lambda_action_on_process \
    --capabilities CAPABILITY_IAM

if [ $? -ne 0 ]; then
    echo "An unexpected error deploying. I can't handle it. =("
    echo "Keeping the packaged template."
    exit 1
fi

rm -f $packaged_tmp_template

echo

bucket=$(aws cloudformation describe-stack-resources --stack-name $stackname --query 'StackResources[?LogicalResourceId==`myBucket`].PhysicalResourceId' --out text)

endpoint=$(aws cloudformation describe-stacks --stack-name $stackname --query 'Stacks[0].Outputs[?OutputKey==`ElasticEndpoint`].OutputValue' --out text)

echo "Your bucket name is $bucket"
echo "You ElasticSearch endpoint is: $endpoint"
echo "* Please remember that you need authentication to connect to the endpoint."