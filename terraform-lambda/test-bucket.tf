resource "random_pet" "openadr-device_bucket_name" {
  prefix = "openadr-device"
  length = 2
}

resource "aws_s3_bucket" "openadr-device" {
  bucket        = random_pet.openadr-device_bucket_name.id
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "openadr-device" {
  bucket = aws_s3_bucket.openadr-device.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "openadr-device" {
  bucket = aws_s3_bucket.openadr-device.id

  key     = "openadr_devices.json"
  content = jsonencode({ name = "S3" })
}

output "openadr-device_s3_bucket" {
  value = random_pet.openadr-device_bucket_name.id
}