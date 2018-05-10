import json
from boto3.session import Session
from botocore.client import Config

session = Session()
config = Config(connect_timeout=10, read_timeout=310)
client = session.client('lambda', config=config)

lambda_payload = {
    # 'locustfile': 'postsearch_locust.py',
    'classes': ['SearchUser2'],
    'host': 'https://tsmith1.ucsc-cgp-dev.org/v1/',
    'num_requests': '100',
    'num_clients': '5',
    'hatch_rate': '1'
}
response = client.invoke(FunctionName='lambda_locust', Payload=json.dumps(lambda_payload))
# response = client.invoke(FunctionName='dss-scale-test', Payload=json.dumps(lambda_payload))
print(json.loads(response['Payload'].read()))