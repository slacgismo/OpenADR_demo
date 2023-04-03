resource "aws_iam_role" "lambda_meters_lambda_exec" {
  # name = "battery_api-lambda"
  name           = "${var.prefix}-${var.client}-${var.environment}-meters-lambda-exec-role"
  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "lambda_meters_lambda_policy" {
  role       = aws_iam_role.lambda_meters_lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}


# S3 policy access
resource "aws_iam_role_policy_attachment" "lambda_meters_lamda_access_s3" {
  role       = aws_iam_role.lambda_meters_lambda_exec.name
  policy_arn = aws_iam_policy.TESS_lambda_s3_access.arn
}


# DynamoDB policy access
resource "aws_iam_role_policy_attachment" "lambda_meters_dynamodb_access" {
  role       = aws_iam_role.lambda_meters_lambda_exec.name
  policy_arn = aws_iam_policy.TESS_lambda_dyanmodb_access.arn
}


resource "aws_lambda_function" "lambda_meters" {
  # function_name = "battery_api"
  function_name ="${var.prefix}-${var.client}-${var.environment}-meters-pai"
  
  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_meters.key
  runtime = "python3.9"
#   runtime = "nodejs16.x"
  handler = "function.handler"

  source_code_hash = data.archive_file.lambda_meters.output_base64sha256

  role = aws_iam_role.lambda_meters_lambda_exec.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_meters" {
  name = "/aws/lambda/${aws_lambda_function.lambda_meters.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_meters" {
  type = "zip"

  source_dir  = "${path.module}/meters"
  output_path = "${path.module}templates/lambda_meters.zip"
}

resource "aws_s3_object" "lambda_meters" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "battery_api.zip"
  source = data.archive_file.lambda_meters.output_path

  etag = filemd5(data.archive_file.lambda_meters.output_path)
}