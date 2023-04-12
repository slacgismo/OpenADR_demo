resource "random_pet" "batteries_bucket_name" {
  prefix = "openadr-batteries"
  length = 2
}

resource "aws_s3_bucket" "batteries" {
  bucket        = random_pet.batteries_bucket_name.id
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "batteries" {
  bucket = aws_s3_bucket.batteries.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "openadr-device_s3_bucket" {
  value = random_pet.batteries_bucket_name.id
}

