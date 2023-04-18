resource "aws_iam_role" "lambda_orders" {
  name = "${var.prefix}-${var.client}-${var.environment}-orders-exec-role"

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

resource "aws_iam_role_policy_attachment" "lambda_orders" {
  role       = aws_iam_role.lambda_orders.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# S3 access
resource "aws_iam_role_policy_attachment" "orders_lamda_access_s3" {
  role       = aws_iam_role.lambda_orders.name
  policy_arn = aws_iam_policy.TESS_lambda_s3_access.arn
}


# DynamoDB access
resource "aws_iam_role_policy_attachment" "lambda_orders_dynamodb_access" {
  role       = aws_iam_role.lambda_orders.name
  policy_arn = aws_iam_policy.TESS_lambda_dyanmodb_access.arn
}


resource "aws_lambda_function" "lambda_orders" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-orders-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_orders.key
  runtime   = "python3.9"
  # runtime = "nodejs16.x"
  handler = "function.handler"

  source_code_hash = data.archive_file.lambda_orders.output_base64sha256

  environment {
    variables = {
      "ORDERS_TIMESTEAM_TABLE_NAME" = aws_timestreamwrite_table.orders.name
      "TIMESTREAM_DB_NAME" = aws_timestreamwrite_database.measurements.name
    }
  }

  role = aws_iam_role.lambda_orders.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_orders" {
  name = "/aws/lambda/${aws_lambda_function.lambda_orders.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_orders" {
  type = "zip"

  source_dir  = "${path.module}/orders"
  output_path = "${path.module}/templates/orders.zip"
}

resource "aws_s3_object" "lambda_orders" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "lambda_orders.zip"
  source = data.archive_file.lambda_orders.output_path

  etag = filemd5(data.archive_file.lambda_orders.output_path)
}