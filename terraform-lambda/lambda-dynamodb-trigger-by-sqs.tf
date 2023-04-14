




data "archive_file" "lambda_sqs_event" {
  type = "zip"

  source_dir  = "${path.module}/lambda-dynamodb-trigger-by-sqs"
  output_path = "${path.module}/templates/lambda-dynamodb-trigger-by-sqs.zip"
}


resource "aws_s3_object" "lambda_sqs_event_s3_key" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "lambda-dynamodb-event-trigger.zip"
  source = data.archive_file.lambda_sqs_event.output_path

  etag = filemd5(data.archive_file.lambda_sqs_event.output_path)
}




resource "aws_lambda_function" "lambda_sqs_event" {
   
  function_name = "${var.prefix}-${var.client}-${var.environment}-lambda_sqs_event"

  runtime   = "python3.9"

#   runtime = "nodejs16.x"
  handler = "function.handler"

  environment {
    variables = {
        "FROM_EVENT_QUEUE_URL" = aws_sqs_queue.device_table_event_sqs.id,
        "TO_TRIGGER_QUEUE_URL" = aws_sqs_queue.opneadr_workers_sqs.id
        "MARKETS_TABLE" = aws_dynamodb_table.markets.name
        "AGENTS_TABLE" = aws_dynamodb_table.agents.name
        "SETTINGS_TABLE" =aws_dynamodb_table.settings.name
        "METERS_TABLE" =aws_dynamodb_table.meters.name
    }
  }
  # local file
  #  filename      = "lambda-dynamodb-trigger-by-sqs.zip"
  # source_code_hash = data.archive_file.lambda_sqs_event.output_base64sha256
  # S3 file
  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_sqs_event_s3_key.key
  
  source_code_hash = data.archive_file.lambda_sqs_event.output_base64sha256
  role = aws_iam_role.lambda_sqs_event.arn
  tags = local.common_tags
}

resource "aws_iam_role" "lambda_sqs_event" {
  name = "lambda_sqs_event_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}




resource "aws_iam_role_policy_attachment" "lambda_sqs_event_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_sqs_event.name
}


# grant sqs permission to invoke lambda
resource "aws_lambda_permission" "sqs_lambda_permission" {
  statement_id  = "AllowExecutionFromSQS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_sqs_event.function_name
  principal     = "sqs.amazonaws.com"

  source_arn = aws_sqs_queue.device_table_event_sqs.arn
}


resource "aws_lambda_event_source_mapping" "lambda_sqs_event_source_mapping" {
  event_source_arn = aws_sqs_queue.device_table_event_sqs.arn
  function_name    = aws_lambda_function.lambda_sqs_event.function_name
  
}

resource "aws_iam_policy" "lambda_sqs_policy" {
  name        = "lambda-sqs-policy"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_sqs_policy_attachment" {
  policy_arn = aws_iam_policy.lambda_sqs_policy.arn
  role       = aws_iam_role.lambda_sqs_event.name
}


