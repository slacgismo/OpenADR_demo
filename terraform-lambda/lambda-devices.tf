

resource "aws_lambda_function" "lambda_devices" {

  function_name = "${var.prefix}-${var.client}-${var.environment}-devices-api"
  s3_bucket     = aws_s3_bucket.lambda_bucket.id
  s3_key        = aws_s3_object.lambda_devices.key
  runtime       = "python3.9"
  handler = "function.handler"

  source_code_hash = data.archive_file.lambda_devices.output_base64sha256
  environment {
      variables = {
          "DEVICES_TABLE_NAME" = aws_dynamodb_table.devices.name
    }
  }


  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_devices" {
  name = "/aws/lambda/${aws_lambda_function.lambda_devices.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_devices" {
  type = "zip"

  source_dir  = "${path.module}/lambda_functions/devices"
  output_path = "${path.module}/templates/devices.zip"
}

resource "aws_s3_object" "lambda_devices" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "devices.zip"
  source = data.archive_file.lambda_devices.output_path

  etag = filemd5(data.archive_file.lambda_devices.output_path)
}


# # S3 policy access
# resource "aws_iam_role_policy_attachment" "lambda_devices_s3_access" {
#   role       = aws_iam_role.lambda_devices.name
#   policy_arn = aws_iam_policy.TESS_lambda_s3_access.arn
# }

# # Dynamodb policy access
# resource "aws_iam_role_policy_attachment" "lambda_devices_dynamodb_access" {
#   role       = aws_iam_role.lambda_devices.name
#   policy_arn = aws_iam_policy.TESS_lambda_dyanmodb_access.arn
# }
