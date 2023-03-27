resource "aws_s3_bucket" "agents" {
  bucket        = lower("shared.${var.client}-${var.environment}.tf-state")
  force_destroy = true
  tags          = local.common_tags
}

resource "aws_s3_bucket_public_access_block" "agents" {
  bucket = aws_s3_bucket.agents.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "batteries_bucket_name" {
  value = aws_s3_bucket.agents.bucket
}