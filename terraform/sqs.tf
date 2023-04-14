

data "aws_sqs_queue" "opneadr_workers_sqs" {
  name ="openadr-NHEC-dev-workers-sqs.fifo"
}

data "aws_sqs_queue" "worker_dlq" {
  name = "openadr-NHEC-dev-workers-dlq.fifo"
}


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



# output "opneadr_workers_sqs_url" {
#   value = aws_sqs_queue.opneadr_workers_sqs.url
# }

# output "openadr_workers_dlq_url" {
#   value = aws_sqs_queue.worker_dlq.url
# }