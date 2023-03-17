data "aws_cloudwatch_log_group" "openadr_logs" {
  name = var.cloudwatch_name
}

