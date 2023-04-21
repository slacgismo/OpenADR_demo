

resource "aws_lambda_function" "lambda_settlements" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-settlements-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_settlements.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"

  source_code_hash = data.archive_file.lambda_settlements.output_base64sha256

  environment {
    variables = {
      "SETTLEMENTS_TABLE_NAME" = aws_dynamodb_table.settlements.name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_settlements" {
  name = "/aws/lambda/${aws_lambda_function.lambda_settlements.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_settlements" {
  type = "zip"

  source_dir  = "${path.module}/lambda_functions/settlements"
  output_path = "${path.module}/templates/settlements.zip"
}

resource "aws_s3_object" "lambda_settlements" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "settlements.zip"
  source = data.archive_file.lambda_settlements.output_path

  etag = filemd5(data.archive_file.lambda_settlements.output_path)
}