

resource "aws_s3_bucket" "lambda_bucket" {
  bucket        =  lower("${var.client}-${var.environment}.lambdabucket")
  force_destroy = true
  tags = local.common_tags
}

resource "aws_s3_bucket_public_access_block" "lambda_bucket" {
  bucket = aws_s3_bucket.lambda_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}