resource "aws_sqs_queue" "device_sqs" {
  name = "${var.prefix}-${var.client}-${var.environment}-devices-sqs"

  tags = local.common_tags
}
