{
    "Statement": [
        {

            "Action": [
                "sqs:ReceiveMessage",
                "sqs:SendMessage",
                "sqs:DeleteMessage"
            ],
            "Effect": "Allow",
            "Resource": [
                "${fifo_sqs_arn}",
                "${fifo_dlq_sqs_arn}"
            ],
            "Sid": "AllowSQSActions"
        }
    ],
    "Version": "2012-10-17"
}