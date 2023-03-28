# resource "aws_iam_role" "battery_api_lambda_exec" {
#   # name = "battery_api-lambda"
#   name           = "${var.prefix}-${var.client}-${var.environment}-mock-battery-lambda-exec-role"
#   assume_role_policy = <<POLICY
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Principal": {
#         "Service": "lambda.amazonaws.com"
#       },
#       "Action": "sts:AssumeRole"
#     }
#   ]
# }
# POLICY
# }

# resource "aws_iam_role_policy_attachment" "battery_api_lambda_policy" {
#   role       = aws_iam_role.battery_api_lambda_exec.name
#   policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
# }


# resource "aws_iam_policy" "dyanmodb_lambda_access" {
#   depends_on = [aws_dynamodb_table.battery-table]
#   # name = "dyanmodb_lambda_access"
#   name           = "${var.prefix}-${var.client}-${var.environment}-dynamodb-lambda-access-ploicy"
#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Action = [
#           "dynamodb:BatchGetItem",
#           "dynamodb:GetItem",
#           "dynamodb:Query",
#           "dynamodb:Scan",
#           "dynamodb:BatchWriteItem",
#           "dynamodb:PutItem",
#           "dynamodb:UpdateItem",
#         ]
#         Effect   = "Allow"
#         "Resource": "${aws_dynamodb_table.battery-table.arn}"
#       },
#     ]
#   })
# }

# resource "aws_iam_role_policy_attachment" "dyanmodb_lambda_access_attach" {
#   role       = aws_iam_role.battery_api_lambda_exec.name
#   policy_arn = aws_iam_policy.dyanmodb_lambda_access.arn
# }



# resource "aws_iam_role_policy_attachment" "battery_api_lamda_access_s3" {
#   role       = aws_iam_role.battery_api_lambda_exec.name
#   policy_arn = aws_iam_policy.test_s3_bucket_access.arn
# }

# resource "aws_lambda_function" "battery_api" {
#   # function_name = "battery_api"
#   function_name ="${var.prefix}-${var.client}-${var.environment}-mock-battery-pai"
  
#   s3_bucket = aws_s3_bucket.lambda_bucket.id
#   s3_key    = aws_s3_object.lambda_battery_api.key

#   runtime = "nodejs16.x"
#   handler = "function.handler"

#   source_code_hash = data.archive_file.lambda_battery_api.output_base64sha256

#   role = aws_iam_role.battery_api_lambda_exec.arn
#   tags = local.common_tags
# }

# resource "aws_cloudwatch_log_group" "battery_api" {
#   name = "/aws/lambda/${aws_lambda_function.battery_api.function_name}"

#   retention_in_days = 14
# }

# data "archive_file" "lambda_battery_api" {
#   type = "zip"

#   source_dir  = "${path.module}/battery_api"
#   output_path = "${path.module}/battery_api.zip"
# }

# resource "aws_s3_object" "lambda_battery_api" {
#   bucket = aws_s3_bucket.lambda_bucket.id

#   key    = "battery_api.zip"
#   source = data.archive_file.lambda_battery_api.output_path

#   etag = filemd5(data.archive_file.lambda_battery_api.output_path)
# }