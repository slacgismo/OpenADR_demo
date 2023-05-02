# resource "aws_s3_bucket" "lambda_bucket" {
#   bucket        = lower("${var.client}-${var.environment}.shared.lambda")
#   force_destroy = true
#   tags          = local.common_tags
# }

