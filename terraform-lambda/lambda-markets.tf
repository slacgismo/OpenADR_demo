

resource "aws_lambda_function" "lambda_markets" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-markets-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_markets.key
  runtime   = "python3.9"
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]
  timeout       = 60
  memory_size   = 128
  source_code_hash = data.archive_file.lambda_markets.output_base64sha256

  environment {
    variables = {
      "MARKETS_TABLE_NAME" = aws_dynamodb_table.markets.name
      "MARKETS_TABLE_RESOURCE_ID_VALID_AT_GSI" =  element(tolist(aws_dynamodb_table.markets.global_secondary_index), 0).name
      "MARKETS_TABLE_STATUS_VALID_AT_GSI" =  element(tolist(aws_dynamodb_table.markets.global_secondary_index), 1).name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_markets" {
  name = "/aws/lambda/${aws_lambda_function.lambda_markets.function_name}"

  retention_in_days = 14
  tags = local.common_tags
}

data "archive_file" "lambda_markets" {
  type = "zip"

  source_dir  = "${path.module}/api/markets"
  output_path = "${path.module}/templates/markets.zip"
}

resource "aws_s3_object" "lambda_markets" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "markets.zip"
  source = data.archive_file.lambda_markets.output_path

  etag = filemd5(data.archive_file.lambda_markets.output_path)
}