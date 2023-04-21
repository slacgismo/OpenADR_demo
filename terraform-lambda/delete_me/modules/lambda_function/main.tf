resource "aws_iam_role" "lambda" {
  name = "${var.prefix}-${var.client}-${var.environment}-"${var.lambda_function_name}"-exec-role"

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

resource "aws_iam_role_policy_attachment" "lambda" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# S3 access
resource "aws_iam_role_policy_attachment" "orders_lamda_access_s3" {
  role       = aws_iam_role.lambda.name
  policy_arn = var.lambda_s3_access_policy_arn
}


# DynamoDB access
resource "aws_iam_role_policy_attachment" "lambda_orders_dynamodb_access" {
  role       = aws_iam_role.lambda.name
  policy_arn =var.lambda_dynamodb_access_policy_arn
}


# Timestream access
resource "aws_iam_role_policy_attachment" "lambda_orders_dynamodb_access" {
  role       = aws_iam_role.lambda.name
  policy_arn =var.lambda_timestream_access_policy_arn
}

resource "aws_lambda_function" "lambda" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-"{var.lambda_function_name}"-api"

  s3_bucket = var.lambda_function_s3_bucket_id
  s3_key    =  aws_s3_object.lambda.key
  runtime   = var.lambda_runtime
  memory_size = var.lambda_memory_size
  handler =  var.lambda_handler

  source_code_hash = data.archive_file.lambda_orders.output_base64sha256

  environment {
    variables = var.lambda_environment_variables
  }

  role = aws_iam_role.lambda.arn
  tags = var.tags
}

resource "aws_cloudwatch_log_group" "lambda" {
  name = "/aws/lambda/${var.lambda_function_name}"

  retention_in_days = var.lambda_log_retention_in_days
}

data "archive_file" "lambda" {
  type = "zip"

  source_dir  = "${path.module}/${var.lambda_function_path}"
  output_path = "${path.module}/templates/${var.lambda_function_name}.zip"
}

resource "aws_s3_object" "lambda" {
  bucket = var.lambda_function_s3_bucket_id

  key    = "${var.lambda_function_name}.zip"
  source = data.archive_file.lambda.output_path

  etag = filemd5(data.archive_file.lambda.output_path)
}