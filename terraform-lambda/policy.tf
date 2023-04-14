# resource "aws_iam_policy" "TESS_lambda_dyanmodb_access" {
#   depends_on = [aws_dynamodb_table.devices, aws_dynamodb_table.orders, aws_dynamodb_table.dispatches]
#   # name = "dyanmodb_lambda_access"
#   name           = "${var.prefix}-${var.client}-${var.environment}-lambda-dynamodb-limit-access-ploicy"
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
#         "Resource": [   "${aws_dynamodb_table.devices.arn}",
#                         "${aws_dynamodb_table.orders.arn}",
#                         "${aws_dynamodb_table.meters.arn}",
#                         "${aws_dynamodb_table.dispatches.arn}"]
#       },
#     ]
#   })
# }


resource "aws_iam_policy" "TESS_lambda_dyanmodb_access" {
  depends_on = [aws_dynamodb_table.devices, aws_dynamodb_table.orders, aws_dynamodb_table.dispatches]
  # name = "dyanmodb_lambda_access"
  name = "${var.prefix}-${var.client}-${var.environment}-lambda-dynamodb-limit-access-ploicy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:BatchGetItem",
          "dynamodb:GetItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchWriteItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "timestream:WriteRecords",
          "timestream:DescribeTable",
          "timestream:ListMeasures",
          "timestream:Select"
        ]
        Effect = "Allow"
        "Resource" : "*"
      },
    ]
  })
}


resource "aws_iam_policy" "TESS_lambda_s3_access" {
  name = "${var.prefix}-${var.client}-${var.environment}-lambda-s3-limit-access-ploicy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:s3:::${aws_s3_bucket.lambda_bucket.id}/*"
      },
    ]
  })

}


