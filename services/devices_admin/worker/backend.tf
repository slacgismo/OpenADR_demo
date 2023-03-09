terraform {
  backend "s3" {
    bucket         = var.backend_bucket
    key            =  var.backend_bucket_key
    region         = var.aws_region
    encrypt        = true
    dynamodb_table = var.dynamodb_table_lock
  }
}