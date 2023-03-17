resource "aws_iam_role" "openadr_devices_lambda_exec" {
  name = "openadr_devices-lambda"

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

resource "aws_iam_role_policy_attachment" "openadr_devices_lambda_policy" {
  role       = aws_iam_role.openadr_devices_lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy" "test_s3_bucket_access" {
  name = "TestS3BucketAccess"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:s3:::${aws_s3_bucket.batteries.id}/*"
      },
    ]
  })
  
}

resource "aws_iam_role_policy_attachment" "s3_lambda_test_s3_bucket_access" {
  role       = aws_iam_role.openadr_devices_lambda_exec.name
  policy_arn = aws_iam_policy.test_s3_bucket_access.arn
}


resource "aws_lambda_function" "openadr_devices" {
  function_name = "openadr_devices"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_openadr_devices.key

  runtime = "nodejs16.x"
  handler = "function.handler"

  source_code_hash = data.archive_file.lambda_openadr_devices.output_base64sha256

  role = aws_iam_role.openadr_devices_lambda_exec.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "openadr_devices" {
  name = "/aws/lambda/${aws_lambda_function.openadr_devices.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_openadr_devices" {
  type = "zip"

  source_dir  = "${path.module}/openadr_devices"
  output_path = "${path.module}/openadr_devices.zip"
}

resource "aws_s3_object" "lambda_openadr_devices" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "openadr_devices.zip"
  source = data.archive_file.lambda_openadr_devices.output_path

  etag = filemd5(data.archive_file.lambda_openadr_devices.output_path)
}