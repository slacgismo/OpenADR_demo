

resource "aws_lambda_function" "lambda_weather" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-weather-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_weather.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"

  source_code_hash = data.archive_file.lambda_weather.output_base64sha256

  environment {
    variables = {
      "WEATHER_TABLE_NAME" = aws_dynamodb_table.weather.name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_weather" {
  name = "/aws/lambda/${aws_lambda_function.lambda_weather.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_weather" {
  type = "zip"

  source_dir  = "${path.module}/lambda_functions/weather"
  output_path = "${path.module}/templates/weather.zip"
}

resource "aws_s3_object" "lambda_weather" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "weather.zip"
  source = data.archive_file.lambda_weather.output_path

  etag = filemd5(data.archive_file.lambda_weather.output_path)
}