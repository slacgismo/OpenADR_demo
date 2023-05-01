


resource "aws_lambda_function" "lambda_auctions" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-auctions-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_auctions.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]

  source_code_hash = data.archive_file.lambda_auctions.output_base64sha256

  environment {
    variables = {
      "AUCTIONS_TABLE_NAME" = aws_dynamodb_table.auctions.name
      "AUCTIONS_TABLE_MARKET_ID_VALID_AT_GSI" =  element(tolist(aws_dynamodb_table.auctions.global_secondary_index), 0).name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_auctions" {
  name = "/aws/lambda/${aws_lambda_function.lambda_auctions.function_name}"

  retention_in_days = 14
  tags = local.common_tags
}

data "archive_file" "lambda_auctions" {
  type = "zip"

  source_dir  = "${path.module}/api/auctions"
  output_path = "${path.module}/templates/auctions.zip"
}

resource "aws_s3_object" "lambda_auctions" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "auctions.zip"
  source = data.archive_file.lambda_auctions.output_path

  etag = filemd5(data.archive_file.lambda_auctions.output_path)
}


# ---------------------------------------------- #
#  TEST EVENT  Example
# ---------------------------------------------- #


# locals {
#   auctions_test_event = jsondecode(file("${path.module}/api/auctions/event.json"))
# }


# resource "aws_lambda_invocation" "post_auctions" {
#   function_name = aws_lambda_function.lambda_auctions.function_name
#   input         = jsonencode(local.auctions_test_event[2])
# }

# resource "aws_lambda_invocation" "post_auction" {
#   function_name = aws_lambda_function.lambda_auctions.function_name
#   input         = jsonencode(local.auctions_test_event[5])
# }

# resource "aws_lambda_invocation" "query_auctions" {
#   function_name = aws_lambda_function.lambda_auctions.function_name
#   input         = jsonencode(local.auctions_test_event[0])
# }

# resource "aws_lambda_invocation" "scan_auctions" {
#   function_name = aws_lambda_function.lambda_auctions.function_name
#   input         = jsonencode(local.auctions_test_event[1])
# }


# resource "aws_lambda_invocation" "delete_auctions" {
#   function_name = aws_lambda_function.lambda_auctions.function_name
#   input         = jsonencode(local.auctions_test_event[3])
# }
# resource "aws_lambda_invocation" "get_auction" {
#   function_name = aws_lambda_function.lambda_auctions.function_name
#   input         = jsonencode(local.auctions_test_event[4])
# }

# resource "aws_lambda_invocation" "put_auction" {
#   function_name = aws_lambda_function.lambda_auctions.function_name
#   input         = jsonencode(local.auctions_test_event[6])
# }
# resource "aws_lambda_invocation" "delete_auction" {
#   function_name = aws_lambda_function.lambda_auctions.function_name
#   input         = jsonencode(local.auctions_test_event[7])
# }
# output "auctions_test_auctions_test_events_results" {
#   value = {
#     query_auctions = aws_lambda_invocation.query_auctions.result,
#     scan_auctions = aws_lambda_invocation.scan_auctions.result
#     post_auctions = aws_lambda_invocation.post_auctions.result
#     delete_auctions = aws_lambda_invocation.delete_auctions.result
#     get_auction = aws_lambda_invocation.get_auction.result
#     post_auction = aws_lambda_invocation.post_auction.result
#     put_auction = aws_lambda_invocation.put_auction.result
#     delete_auction = aws_lambda_invocation.delete_auction.result
#   }
# }
