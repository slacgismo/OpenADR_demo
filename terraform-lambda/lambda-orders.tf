


resource "aws_lambda_function" "lambda_orders" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-orders-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_orders.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"

  source_code_hash = data.archive_file.lambda_orders.output_base64sha256

  environment {
    variables = {
       "ORDERS_TABLE_NAME" = aws_dynamodb_table.orders.name
      # "ORDERS_TIMESTEAM_TABLE_NAME" = aws_timestreamwrite_table.orders.table_name
      # "TIMESTREAM_DB_NAME" = aws_timestreamwrite_database.measurements.database_name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_orders" {
  name = "/aws/lambda/${aws_lambda_function.lambda_orders.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_orders" {
  type = "zip"

  source_dir  = "${path.module}/lambda_functions/orders"
  output_path = "${path.module}/templates/orders.zip"
}

resource "aws_s3_object" "lambda_orders" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "orders.zip"
  source = data.archive_file.lambda_orders.output_path

  etag = filemd5(data.archive_file.lambda_orders.output_path)
}