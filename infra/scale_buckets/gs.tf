
resource google_storage_bucket dss_gs_scale_bucket {
  name = "${var.DSS_GS_SCALE_BUCKET}"

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = "${var.DSS_BLOB_TTL_DAYS}"
      matches_storage_class = [
        "DURABLE_REDUCED_AVAILABILITY"]
      with_state = "LIVE"
    }

  }
}


