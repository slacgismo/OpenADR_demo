resource "aws_iam_role" "dispatch_exec" {
  name = "${var.prefix}-${var.client}-${var.environment}-dispatch-exec-role"

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

resource "aws_iam_role_policy_attachment" "dispatched_lambda_policy" {
  role       = aws_iam_role.dispatch_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# S3 policy access

resource "aws_iam_role_policy_attachment" "dispatches_lamda_access_s3" {
  role       = aws_iam_role.dispatch_exec.name
  policy_arn = aws_iam_policy.TESS_lambda_s3_access.arn
}
# DynamoDB policy access
resource "aws_iam_role_policy_attachment" "lambda_dispatches_dynamodb_access" {
  role       = aws_iam_role.dispatch_exec.name
  policy_arn = aws_iam_policy.TESS_lambda_dyanmodb_access.arn
}


resource "aws_lambda_function" "dispatches" {
  # function_name = "participated_vens"
  function_name = "${var.prefix}-${var.client}-${var.environment}-dispatch-api"
  s3_bucket     = aws_s3_bucket.lambda_bucket.id
  s3_key        = aws_s3_object.dispatch_vens.key
  runtime       = "python3.9"
  # runtime = "nodejs16.x"
  handler = "function.handler"

  source_code_hash = data.archive_file.dispatch_vens.output_base64sha256
  environment {
      variables = {
          "DISPATCHES_TIMESTREAM_TABLE_NAME" = aws_timestreamwrite_table.dispatches.name
          "TIMESTREAM_DB_NAME"= aws_timestreamwrite_database.measurements.name
    }
  }
  role = aws_iam_role.dispatch_exec.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "participated_vens" {
  name = "/aws/lambda/${aws_lambda_function.dispatches.function_name}"

  retention_in_days = 14
}

data "archive_file" "dispatch_vens" {
  type = "zip"

  source_dir  = "${path.module}/dispatches"
  output_path = "${path.module}/templates/dispatches.zip"
}

resource "aws_s3_object" "dispatch_vens" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "dispatch_vens.zip"
  source = data.archive_file.dispatch_vens.output_path

  etag = filemd5(data.archive_file.dispatch_vens.output_path)
}