data "aws_caller_identity" "current" {}

locals {
  common_tags = "${map(
    "managedBy" , "terraform",
    "Name"      , "${var.DSS_INFRA_TAG_PROJECT}-${var.DSS_DEPLOYMENT_STAGE}-${var.DSS_INFRA_TAG_SERVICE}",
    "project"   , "${var.DSS_INFRA_TAG_PROJECT}",
    "env"       , "${var.DSS_DEPLOYMENT_STAGE}",
    "service"   , "${var.DSS_INFRA_TAG_SERVICE}",
    "owner"     , "${var.DSS_INFRA_TAG_OWNER}"
  )}"
}


resource aws_s3_bucket dss_s3_scale_bucket {
  count = "${length(var.DSS_S3_CHECKOUT_BUCKET) > 0 ? 1 : 0}"
  bucket = "${var.DSS_S3_SCALE_BUCKET}"
  tags = "${local.common_tags}"
  lifecycle_rule {
    id = "failed multipart cleanup"
    enabled = true
    abort_incomplete_multipart_upload_days = "${var.DSS_BLOB_TTL_DAYS}"
  }
}


