

resource "aws_lambda_function" "lambda_swagger" {
  depends_on = [aws_s3_object.openapi_file]
  function_name = "${var.prefix}-${var.client}-${var.environment}-swagger-api"

  s3_bucket = var.meta_data_bucket_name
  s3_key    = aws_s3_object.lambda_swagger.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]
  source_code_hash = data.archive_file.lambda_swagger.output_base64sha256

  environment {
    variables = {
      "S3_BUCKET" = var.meta_data_bucket_name
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

  source_dir  = "../api/swagger"
  output_path = "${path.module}/templates/swagger.zip"
}

# lambda function zip
resource "aws_s3_object" "lambda_swagger" {
  bucket = var.meta_data_bucket_name

  key    = "swagger/swagger.zip"
  source = data.archive_file.lambda_swagger.output_path

  etag = filemd5(data.archive_file.lambda_swagger.output_path)
}

# 
resource "aws_s3_object" "openapi_file" {
  depends_on = [local_file.openapi_json]
  bucket = var.meta_data_bucket_name

  key    = "openapi.json"
  source = "../api/openapi.json"

  etag = filemd5(data.archive_file.lambda_swagger.output_path)
}



