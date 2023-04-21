


resource "aws_lambda_function" "lambda_auctions" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-auctions-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_auctions.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]

  source_code_hash = data.archive_file.lambda_auctions.output_base64sha256

  environment {
    variables = {
      "AUCTIONS_TABLE_NAME" = aws_dynamodb_table.auctions.name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_auctions" {
  name = "/aws/lambda/${aws_lambda_function.lambda_auctions.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_auctions" {
  type = "zip"

  source_dir  = "${path.module}/lambda_functions/auctions"
  output_path = "${path.module}/templates/auctions.zip"
}

resource "aws_s3_object" "lambda_auctions" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "auctions.zip"
  source = data.archive_file.lambda_auctions.output_path

  etag = filemd5(data.archive_file.lambda_auctions.output_path)
}