
resource "aws_lambda_function" "lambda_meters" {
  # function_name = "battery_api"
  function_name = "${var.prefix}-${var.client}-${var.environment}-meters-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_meters.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"

  source_code_hash = data.archive_file.lambda_meters.output_base64sha256
  environment {
    variables = {
      "METERS_TABLE_NAME" = aws_dynamodb_table.meters.name,
      # "READINGS_TIMESTREAM_TABLE_NAME" = aws_timestreamwrite_table.readings.table_name
      # "TIMESTREAM_DB_NAME" = aws_timestreamwrite_database.measurements.database_name
    }
  }
  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_meters" {
  name = "/aws/lambda/${aws_lambda_function.lambda_meters.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_meters" {
  type = "zip"

  source_dir  = "${path.module}/lambda_functions/meters"
  output_path = "${path.module}/templates/meters.zip"
}

resource "aws_s3_object" "lambda_meters" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "meters.zip"
  source = data.archive_file.lambda_meters.output_path

  etag = filemd5(data.archive_file.lambda_meters.output_path)
}