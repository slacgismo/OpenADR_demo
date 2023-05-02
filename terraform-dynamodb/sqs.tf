resource "aws_sqs_queue" "devices_tables_event_sqs" {
  name = "${var.prefix}-${var.client}-${var.environment}-devices-table-event-sqs"

  # redrive_policy = jsonencode({
  #   deadLetterTargetArn = aws_sqs_queue.event_dlq.arn
  #   maxReceiveCount     = 3
  # })
  tags = local.common_tags
}

resource "aws_sqs_queue" "settings_tables_event_sqs" {
  name = "${var.prefix}-${var.client}-${var.environment}-settings-table-event-sqs"

  # redrive_policy = jsonencode({
  #   deadLetterTargetArn = aws_sqs_queue.event_dlq.arn
  #   maxReceiveCount     = 3
  # })
  tags = local.common_tags
}

# resource "aws_sqs_queue" "event_dlq" {
#   name       = "${var.prefix}-${var.client}-${var.environment}-event-dlq"

# }

# resource "aws_sqs_queue" "opneadr_workers_sqs" {
#   depends_on = [aws_sqs_queue.worker_dlq]
#   name       = "${var.prefix}-${var.client}-${var.environment}-workers-sqs.fifo"

#   fifo_queue                  = true
#   content_based_deduplication = true
#   redrive_policy = jsonencode({
#     deadLetterTargetArn = aws_sqs_queue.worker_dlq.arn
#     maxReceiveCount     = 3
#   })
# }



# resource "aws_sqs_queue" "worker_dlq" {
#   name       = "${var.prefix}-${var.client}-${var.environment}-workers-dlq.fifo"
#   fifo_queue = true
# }

# output "device_table_event_sqs" {
#   value = aws_sqs_queue.device_table_event_sqs.url
# }

# output "opneadr_workers_sqs_url" {
#   value = aws_sqs_queue.opneadr_workers_sqs.url
# }

# output "openadr_workers_dlq_url" {
#   value = aws_sqs_queue.worker_dlq.url
# }