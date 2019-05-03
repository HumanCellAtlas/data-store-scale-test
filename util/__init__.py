import os
import boto3
import tempfile
from functools import lru_cache


@lru_cache()
def get_gcp_credentials_file():
    """
    Acquire GCP credentials from AWS secretsmanager and write them to a temporary file.
    A reference to the temporary file is saved in lru_cache so it is not cleaned up
    before a GCP client, which expects a credentials file in the file system, is instantiated.
    Normal usage is local execution. For cloud execution (AWS Lambda, etc.),
    credentials are typically available at GOOGLE_APPLICATION_CREDENTIALS.
    """
    secret_store = os.environ['DSS_SECRETS_STORE']
    stage = os.environ['DSS_DEPLOYMENT_STAGE']
    credentials_secrets_name = os.environ['GOOGLE_APPLICATION_CREDENTIALS_SECRETS_NAME']
    secret_id = f"{secret_store}/{stage}/{credentials_secrets_name}"
    resp = boto3.client("secretsmanager").get_secret_value(SecretId=secret_id)
    tf = tempfile.NamedTemporaryFile("w")
    tf.write(resp['SecretString'])
    tf.flush()
    return tf
