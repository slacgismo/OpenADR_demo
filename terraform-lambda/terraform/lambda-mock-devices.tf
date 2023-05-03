
resource "aws_lambda_function" "lambda_mock_devices" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-mock-devices-api"

  s3_bucket = var.meta_data_bucket_name
  s3_key    = aws_s3_object.lambda_mock_devices.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]

  source_code_hash = data.archive_file.lambda_mock_devices.output_base64sha256

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_mock_devices" {
  name = "/aws/lambda/${aws_lambda_function.lambda_mock_devices.function_name}"

  retention_in_days = 14
  tags = local.common_tags
}

data "archive_file" "lambda_mock_devices" {
  type = "zip"

  source_dir  = "../api/mock_devices"
  output_path = "${path.module}/templates/mock_devices.zip"
}

resource "aws_s3_object" "lambda_mock_devices" {
  bucket = var.meta_data_bucket_name

  key    = "mock_devices/mock_devices.zip"
  source = data.archive_file.lambda_mock_devices.output_path

  etag = filemd5(data.archive_file.lambda_mock_devices.output_path)
}

# Log stream
resource "aws_cloudwatch_log_stream" "lambda_mock_devices" {
  name = "/aws/lambda_logstream/${aws_lambda_function.lambda_mock_devices.function_name}"
  log_group_name = aws_cloudwatch_log_group.lambda_mock_devices.name
}


resource "aws_lambda_permission" "lambda_mock_devices" {
  statement_id  = "AllowExecutionFromCloudWatchLogs"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_mock_devices.function_name

  principal = "logs.${var.aws_region}.amazonaws.com"

  source_arn = aws_cloudwatch_log_group.lambda_mock_devices.arn

}