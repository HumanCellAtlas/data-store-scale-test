# Auto-generated during infra build process.
# Please edit infra/build_deploy_config.py directly.

variable "API_DOMAIN_NAME" {
  default = "dss.dev.data.humancellatlas.org"
}

variable "AWS_DEFAULT_OUTPUT" {
  default = "json"
}

variable "AWS_DEFAULT_REGION" {
  default = "us-east-1"
}

variable "DSS_BLOB_TTL_DAYS" {
  default = "7"
}

variable "ACM_CERTIFICATE_IDENTIFIER" {
  default = "826dbdb8-2b23-4cc9-8fd6-73aa6fc658d7"
}

variable "DSS_CHECKOUT_BUCKET_OBJECT_VIEWERS" {
  default = "serviceAccount:619310558212-compute@developer.gserviceaccount.com,serviceAccount:caas-account@broad-dsde-mint-dev.iam.gserviceaccount.com,serviceAccount:caas-prod-account-for-dev@broad-dsde-mint-dev.iam.gserviceaccount.com"
}

variable "DSS_DEPLOYMENT_STAGE" {
  default = "dev"
}

variable "DSS_ES_DOMAIN" {
  default = "dss-index-dev"
}

variable "DSS_ES_DOMAIN_INDEX_LOGS_ENABLED" {
  default = "true"
}

variable "DSS_ES_INSTANCE_COUNT" {
  default = "2"
}

variable "DSS_ES_INSTANCE_TYPE" {
  default = "m4.large.elasticsearch"
}

variable "DSS_ES_VOLUME_SIZE" {
  default = "35"
}

variable "DSS_GCP_SERVICE_ACCOUNT_NAME" {
  default = "travis-test"
}

variable "DSS_GS_BUCKET" {
  default = "org-humancellatlas-dss-dev"
}

variable "DSS_GS_BUCKET_INTEGRATION" {
  default = "org-humancellatlas-dss-integration"
}

variable "DSS_GS_BUCKET_PROD" {
  default = "org-humancellatlas-dss-prod"
}

variable "DSS_GS_BUCKET_STAGING" {
  default = "org-humancellatlas-dss-staging"
}

variable "DSS_GS_BUCKET_TEST" {
  default = "org-hca-dss-test"
}

variable "DSS_GS_BUCKET_TEST_FIXTURES" {
  default = "org-hca-dss-test-fixtures"
}

variable "DSS_GS_CHECKOUT_BUCKET" {
  default = "org-humancellatlas-dss-checkout-dev"
}

variable "DSS_GS_CHECKOUT_BUCKET_PROD" {
  default = "org-humancellatlas-dss-checkout-prod"
}

variable "DSS_GS_CHECKOUT_BUCKET_STAGING" {
  default = "org-humancellatlas-dss-checkout-staging"
}

variable "DSS_GS_CHECKOUT_BUCKET_TEST" {
  default = "org-hca-dss-checkout-test"
}

variable "DSS_GS_CHECKOUT_BUCKET_TEST_USER" {
  default = "org-hca-dss-checkout-test-user"
}

variable "DSS_INFRA_TAG_PROJECT" {
  default = "dcp"
}

variable "DSS_INFRA_TAG_SERVICE" {
  default = "dss"
}

variable "DSS_INFRA_TAG_OWNER" {
  default = "dss-team@data.humancellatlas.org"
}

variable "DSS_S3_BUCKET" {
  default = "org-humancellatlas-dss-dev"
}

variable "DSS_S3_BUCKET_INTEGRATION" {
  default = "org-humancellatlas-dss-integration"
}

variable "DSS_S3_BUCKET_PROD" {
  default = "org-humancellatlas-dss-prod"
}

variable "DSS_S3_BUCKET_STAGING" {
  default = "org-humancellatlas-dss-staging"
}

variable "DSS_S3_BUCKET_TEST" {
  default = "org-hca-dss-test"
}

variable "DSS_S3_BUCKET_TEST_FIXTURES" {
  default = "org-hca-dss-test-fixtures"
}

variable "DSS_S3_CHECKOUT_BUCKET" {
  default = "org-humancellatlas-dss-checkout-dev"
}

variable "DSS_S3_CHECKOUT_BUCKET_INTEGRATION" {
  default = "org-humancellatlas-dss-checkout-integration"
}

variable "DSS_S3_CHECKOUT_BUCKET_PROD" {
  default = "org-humancellatlas-dss-checkout-prod"
}

variable "DSS_S3_CHECKOUT_BUCKET_STAGING" {
  default = "org-humancellatlas-dss-checkout-staging"
}

variable "DSS_S3_CHECKOUT_BUCKET_TEST" {
  default = "org-hca-dss-checkout-test"
}

variable "DSS_S3_CHECKOUT_BUCKET_TEST_USER" {
  default = "org-hca-dss-checkout-test-user"
}

variable "DSS_S3_CHECKOUT_BUCKET_UNWRITABLE" {
  default = "org-hca-dss-checkout-unwritable"
}

variable "DSS_SECRETS_STORE" {
  default = "dcp/dss"
}

variable "DSS_ZONE_NAME" {
  default = "dev.data.humancellatlas.org."
}

variable "ES_ALLOWED_SOURCE_IP_SECRETS_NAME" {
  default = "es_source_ip"
}

variable "GCP_DEFAULT_REGION" {
  default = "us-central1"
}
