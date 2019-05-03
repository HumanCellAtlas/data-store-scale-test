# Auto-generated during infra build process.
# Please edit infra/build_deploy_config.py directly.
terraform {
  backend "s3" {
    bucket = "org-humancellatlas-dss-861229788715-dev-terraform"
    key = "buckets-dev.tfstate"
    region = "us-east-1"
    
  }
}
