resource "aws_iam_role" "participated_vens_lambda_exec" {
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

resource "aws_iam_role_policy_attachment" "participated_vens_lambda_policy" {
  role       = aws_iam_role.participated_vens_lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}



resource "aws_iam_role_policy_attachment" "participated_vens_lamda_access_s3" {
  role       = aws_iam_role.participated_vens_lambda_exec.name
  policy_arn = aws_iam_policy.test_s3_bucket_access.arn
}

resource "aws_lambda_function" "participated_vens" {
  # function_name = "participated_vens"
  function_name ="${var.prefix}-${var.client}-${var.environment}-dispatch-api"
  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_participated_vens.key

  runtime = "nodejs16.x"
  handler = "function.handler"

  source_code_hash = data.archive_file.lambda_participated_vens.output_base64sha256

  role = aws_iam_role.participated_vens_lambda_exec.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "participated_vens" {
  name = "/aws/lambda/${aws_lambda_function.participated_vens.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_participated_vens" {
  type = "zip"

  source_dir  = "${path.module}/participated_vens"
  output_path = "${path.module}/participated_vens.zip"
}

resource "aws_s3_object" "lambda_participated_vens" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "participated_vens.zip"
  source = data.archive_file.lambda_participated_vens.output_path

  etag = filemd5(data.archive_file.lambda_participated_vens.output_path)
}