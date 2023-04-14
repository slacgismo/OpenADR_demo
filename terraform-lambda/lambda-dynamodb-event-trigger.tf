
data "archive_file" "lambda_dynamodb_event_trigger" {
  type = "zip"

  source_dir  = "${path.module}/lambda-dynamodb-event-trigger"
  output_path = "${path.module}/templates/lambda-dynamodb-event-trigger.zip"
}

resource "aws_s3_object" "lambda_dynamodb_event_trigger_key" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "lambda-dynamodb-event-trigger.zip"
  source = data.archive_file.lambda_dynamodb_event_trigger.output_path

  etag = filemd5(data.archive_file.lambda_dynamodb_event_trigger.output_path)
}




resource "aws_iam_role" "lambda_dynamodb_event_trigger" {
  name = "${var.prefix}-${var.client}-${var.environment}-lambda_dynamodb_event_trigger-exec-role"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_event_trigger" {
  role       = aws_iam_role.lambda_dynamodb_event_trigger.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}




resource "aws_iam_policy" "lambda_dynamodb_event_trigger_policy" {
  name = "${var.prefix}-${var.client}-${var.environment}-lambda-dynamodb-event-trigger-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetRecords",
          "dynamodb:GetShardIterator",
          "dynamodb:DescribeStream",
          "dynamodb:ListStreams"
        ]
        Resource = aws_dynamodb_table.devices.stream_arn
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_event_trigger_stream" {
  role       = aws_iam_role.lambda_dynamodb_event_trigger.name
  policy_arn = aws_iam_policy.lambda_dynamodb_event_trigger_policy.arn
}


resource "aws_iam_policy" "lambda_dynamodb_sqs_trigger_policy" {
  name = "${var.prefix}-${var.client}-${var.environment}-lambda-dynamodb-sqs-trigger-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage", 
          "sqs:SendMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
          ]
        Resource = aws_sqs_queue.device_sqs.arn
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_event_trigger_sqs" {
  role       = aws_iam_role.lambda_dynamodb_event_trigger.name
  policy_arn = aws_iam_policy.lambda_dynamodb_sqs_trigger_policy.arn
}



resource "aws_lambda_function" "lambda_dynamodb_event_trigger" {
   
  function_name = "${var.prefix}-${var.client}-${var.environment}-lambda-dynamodb-event-trigger"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_dynamodb_event_trigger_key.key
  runtime   = "python3.9"

#   runtime = "nodejs16.x"
  handler = "function.handler"

  environment {
    variables = {
        "SQS_QUEUE_URL" = aws_sqs_queue.device_sqs.url
    }
  }
    source_code_hash = data.archive_file.lambda_dynamodb_event_trigger.output_base64sha256

  role = aws_iam_role.lambda_dynamodb_event_trigger.arn
  tags = local.common_tags
}
