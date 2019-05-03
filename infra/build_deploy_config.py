#!/usr/bin/env python
import os
import sys
import boto3
import argparse
from google.cloud.storage import Client

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, pkg_root) # noqa

from util import get_gcp_credentials_file


GCP_PROJECT_ID = Client().project
infra_root = os.path.abspath(os.path.dirname(__file__))


if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = get_gcp_credentials_file().name

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("component")
args = parser.parse_args()


terraform_variable_template = """
variable "{name}" {{
  default = "{val}"
}}
"""

terraform_backend_template = """# Auto-generated during infra build process.
# Please edit infra/build_deploy_config.py directly.
terraform {{
  backend "s3" {{
    bucket = "{bucket}"
    key = "{comp}-{stage}.tfstate"
    region = "{region}"
    {profile_setting}
  }}
}}
"""

terraform_providers_template = """# Auto-generated during infra build process.
# Please edit infra/build_deploy_config.py directly.
provider aws {{
  region = "{aws_region}"
}}

provider google {{
  project = "{gcp_project_id}"
}}
"""

env_vars_to_infra = [
    "AWS_DEFAULT_REGION",
    "DSS_BLOB_TTL_DAYS",
    "DSS_BLOB_PUBLIC_TTL_DAYS",
    "DSS_DEPLOYMENT_STAGE",
    "DSS_INFRA_TAG_PROJECT",
    "DSS_INFRA_TAG_SERVICE",
    "DSS_INFRA_TAG_OWNER",
    "DSS_S3_CHECKOUT_BUCKET",
    "DSS_GS_CHECKOUT_BUCKET",
    "DSS_S3_SCALE_BUCKET",
    "DSS_GS_SCALE_BUCKET",
    "API_DOMAIN_NAME",
    "DSS_SECRETS_STORE",
    "GOOGLE_APPLICATION_CREDENTIALS",
    "TARGET_URL"
]

with open(os.path.join(infra_root, args.component, "backend.tf"), "w") as fp:
    caller_info = boto3.client("sts").get_caller_identity()
    if os.environ.get('AWS_PROFILE'):
        profile = os.environ['AWS_PROFILE']
        profile_setting = f'profile = "{profile}"'
    else:
        profile_setting = ''
    fp.write(terraform_backend_template.format(
        bucket=os.environ['DSS_TERRAFORM_BACKEND_BUCKET_TEMPLATE'].format(account_id=caller_info['Account']),
        comp=args.component,
        stage=os.environ['DSS_DEPLOYMENT_STAGE'],
        region=os.environ['AWS_DEFAULT_REGION'],
        profile_setting=profile_setting,
    ))

with open(os.path.join(infra_root, args.component, "variables.tf"), "w") as fp:
    fp.write("# Auto-generated during infra build process." + os.linesep)
    fp.write("# Please edit infra/build_deploy_config.py directly." + os.linesep)
    for key in env_vars_to_infra:
        val = os.environ[key]
        fp.write(terraform_variable_template.format(name=key, val=val))

with open(os.path.join(infra_root, args.component, "providers.tf"), "w") as fp:
    fp.write(terraform_providers_template.format(
        aws_region=os.environ['AWS_DEFAULT_REGION'],
        gcp_project_id=GCP_PROJECT_ID,
    ))
