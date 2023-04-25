

resource "aws_lambda_function" "lambda_resources" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-resources-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_resources.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"

  source_code_hash = data.archive_file.lambda_resources.output_base64sha256

  environment {
    variables = {
      "RESOURCES_TABLE_NAME" = aws_dynamodb_table.resources.name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_resources" {
  name = "/aws/lambda/${aws_lambda_function.lambda_resources.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_resources" {
  type = "zip"

  source_dir  = "${path.module}/api/resources"
  output_path = "${path.module}/templates/resources.zip"
}

resource "aws_s3_object" "lambda_resources" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "resources.zip"
  source = data.archive_file.lambda_resources.output_path

  etag = filemd5(data.archive_file.lambda_resources.output_path)
}