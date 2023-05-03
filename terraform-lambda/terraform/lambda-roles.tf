resource "aws_iam_role" "lambda_generic_exec_role" {
  name = "${var.prefix}-${var.client}-${var.environment}-lambda-generic-exec-role"

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

resource "aws_iam_role_policy_attachment" "lambda_generic_basic_exec_role" {
  role       = aws_iam_role.lambda_generic_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# S3 access
resource "aws_iam_role_policy_attachment" "lambda_generic_exec_role_s3_access" {
  role       = aws_iam_role.lambda_generic_exec_role.name
  policy_arn = aws_iam_policy.tess_lambda_s3_access.arn
}


# DynamoDB access
resource "aws_iam_role_policy_attachment" "lambda_generic_exec_role_dynamodb_access" {
  role       = aws_iam_role.lambda_generic_exec_role.name
  policy_arn = aws_iam_policy.tess_lambda_dyanmodb_access.arn
}

# Timestream access
resource "aws_iam_role_policy_attachment" "lambda_generic_exec_role_timestream_access" {
  role       = aws_iam_role.lambda_generic_exec_role.name
  policy_arn = aws_iam_policy.tess_lambda_timestream_access.arn
}
