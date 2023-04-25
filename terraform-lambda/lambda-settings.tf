

resource "aws_lambda_function" "lambda_settings" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-settings-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_settings.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]
  source_code_hash = data.archive_file.lambda_settings.output_base64sha256

  environment {
    variables = {
      "SETTINGS_TABLE_NAME" = aws_dynamodb_table.settings.name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_settings" {
  name = "/aws/lambda/${aws_lambda_function.lambda_settings.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_settings" {
  type = "zip"

  source_dir  = "${path.module}/api/settings"
  output_path = "${path.module}/templates/settings.zip"
}

resource "aws_s3_object" "lambda_settings" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "settings.zip"
  source = data.archive_file.lambda_settings.output_path

  etag = filemd5(data.archive_file.lambda_settings.output_path)
}