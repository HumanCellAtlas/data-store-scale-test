lambda:
    docker run -it --volume=$PWD:/project python:3.6 bash -c "pip install -r /project/requirements.txt --target=project/python-packages"
    zip -q -r lambda_locust.zip lambda_locust.py locustfiles locustfile.py python-packages
    aws lambda update-function-code --function-name lambda_locust --zip-file fileb://lambda_locust.zip
    aws lambda update-function-configuration --cli-input-json ./lambda_config.json