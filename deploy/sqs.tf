

resource "aws_sqs_queue" "opneadr_workers_sqs" {
  name = "${var.prefix}_workers_sqs.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
}


output "opneadr_workers_sqs_url" {
  value = aws_sqs_queue.opneadr_workers_sqs.url
}