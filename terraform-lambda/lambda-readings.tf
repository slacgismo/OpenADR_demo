


resource "aws_lambda_function" "lambda_readings" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-readings-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_readings.key
  runtime   = "python3.9"
    timeout       = 60
  memory_size   = 128
  handler = "function.handler"

  source_code_hash = data.archive_file.lambda_readings.output_base64sha256

  environment {
    variables = {
      "READINGS_TABLE_NAME" = aws_dynamodb_table.readings.name
      "READINGS_GLOBAL_SECONDARY_INDEX" = element(tolist(aws_dynamodb_table.readings.global_secondary_index), 0).name
      # "ORDERS_TIMESTEAM_TABLE_NAME" = aws_timestreamwrite_table.orders.table_name
      # "TIMESTREAM_DB_NAME" = aws_timestreamwrite_database.measurements.database_name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_readings" {
  name = "/aws/lambda/${aws_lambda_function.lambda_readings.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_readings" {
  type = "zip"

  source_dir  = "${path.module}/lambda_functions/readings"
  output_path = "${path.module}/templates/readings.zip"
}

resource "aws_s3_object" "lambda_readings" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "readings.zip"
  source = data.archive_file.lambda_readings.output_path

  etag = filemd5(data.archive_file.lambda_orders.output_path)
}