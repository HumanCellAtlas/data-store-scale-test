#!/usr/bin/env bash

if mac:
    if docker is not installed:
        install docker
    docker run -it --volume=$PWD/python-packages:/python-packages python:3.6 bash -c "pip install invokust hca --target=/python-packages"

zip -q -r lambda_locust.zip lambda_locust.py postsearch_locust.py python-packages

# deploy the lambda
aws lambda create-function --function-name lambda_locust --timeout 300 --runtime python3.6 --role arn:aws:iam::719818754276:role/lambda_basic_execution --handler app.handler --zip-file fileb://lambda_locust.zip

#update the lambda's configuration
aws lambda update-function-configuration --function-name lambda_locust --handler app.handler

# update the lambda's code.
aws lambda update-function-code --function-name lambda-locust --zip-file lambda_locust.zip

# invoke the lambda.
aws lambda invoke --function-name lambda_locust --invocation-type RequestResponse --payload '{"locustfile": "postsearch_locust.py", "host":"https://tsmith1.ucsc-cgp-dev.org/v1/", "num_requests":"20", "num_clients": "1", "hatch_rate": "1"}'