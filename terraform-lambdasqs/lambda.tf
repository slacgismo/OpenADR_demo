

data "archive_file" "lambda_sqs_event" {
  type = "zip"

  source_dir  = "${path.module}/lambda_sqs_event"
  output_path = "${path.module}/lambda_sqs_event.zip"
}




resource "aws_lambda_function" "lambda_sqs_event" {
   
  function_name = "${var.prefix}-${var.client}-${var.environment}-lambda_sqs_event"

  runtime   = "python3.9"
  filename      = "lambda_sqs_event.zip"
#   runtime = "nodejs16.x"
  handler = "function.handler"

  environment {
    variables = {
        "SQS_QUEUE_URL" = data.aws_sqs_queue.openadr_sqs.id,
        "SQS_TRIGGER_QUEUE_URL" = data.aws_sqs_queue.create_event_sqs.id
        "MARKETS_TABLE" = 
        "AGENTS_TABLE" =
        "SETTINGS_TABLE" =
        "METERS_TABLE" =
    }
  }
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

data "aws_sqs_queue" "openadr_sqs" {
  name = "openadr-NHEC-dev-devices-sqs"
}
data "aws_sqs_queue" "create_event_sqs" {
  name = "openadr-NHEC-dev-workers-sqs.fifo"
}

# grant sqs permission to invoke lambda
resource "aws_lambda_permission" "sqs_lambda_permission" {
  statement_id  = "AllowExecutionFromSQS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_sqs_event.function_name
  principal     = "sqs.amazonaws.com"

  source_arn = data.aws_sqs_queue.openadr_sqs.arn
}


resource "aws_lambda_event_source_mapping" "lambda_sqs_event_source_mapping" {
  event_source_arn = data.aws_sqs_queue.openadr_sqs.arn
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
