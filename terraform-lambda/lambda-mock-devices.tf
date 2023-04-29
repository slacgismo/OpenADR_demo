
resource "aws_lambda_function" "lambda_mock_devices" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-mock-devices-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
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

  source_dir  = "${path.module}/api/mock_devices"
  output_path = "${path.module}/templates/mock_devices.zip"
}

resource "aws_s3_object" "lambda_mock_devices" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "mock_devices.zip"
  source = data.archive_file.lambda_mock_devices.output_path

  etag = filemd5(data.archive_file.lambda_mock_devices.output_path)
}