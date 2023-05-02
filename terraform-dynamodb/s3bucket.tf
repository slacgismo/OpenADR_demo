

resource "aws_s3_bucket" "meta_data_bucket" {
  bucket        = lower("${var.client}-${var.environment}.shared.metaData")
  force_destroy = true
  tags          = local.common_tags
}

