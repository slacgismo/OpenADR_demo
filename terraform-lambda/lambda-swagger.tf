

resource "aws_lambda_function" "lambda_swagger" {
  depends_on = [aws_s3_object.openapi_file]
  function_name = "${var.prefix}-${var.client}-${var.environment}-swagger-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_swagger.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]
  source_code_hash = data.archive_file.lambda_swagger.output_base64sha256

  environment {
    variables = {
      "S3_BUCKET" = aws_s3_bucket.lambda_bucket.id
      "OPENAPI_KEY" = aws_s3_object.openapi_file.key
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_swagger" {
  name = "/aws/lambda/${aws_lambda_function.lambda_swagger.function_name}"

  retention_in_days = 14
  tags = local.common_tags
}

data "archive_file" "lambda_swagger" {
  type = "zip"

  source_dir  = "${path.module}/api/swagger"
  output_path = "${path.module}/templates/swagger.zip"
}

# lambda function zip
resource "aws_s3_object" "lambda_swagger" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "swagger.zip"
  source = data.archive_file.lambda_swagger.output_path

  etag = filemd5(data.archive_file.lambda_swagger.output_path)
}

# 
resource "aws_s3_object" "openapi_file" {
  depends_on = [local_file.openapi_json]
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "openapi.json"
  source = "${path.module}/api/openapi.json"

  etag = filemd5(data.archive_file.lambda_swagger.output_path)
}



