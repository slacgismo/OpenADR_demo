

resource "aws_lambda_function" "lambda_markets" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-markets-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_markets.key
  runtime   = "python3.9"
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]
  timeout       = 60
  memory_size   = 128
  source_code_hash = data.archive_file.lambda_markets.output_base64sha256

  environment {
    variables = {
      "MARKETS_TABLE_NAME" = var.markets_table_name
      "MARKETS_TABLE_RESOURCE_ID_VALID_AT_GSI" = element(jsondecode(var.markets_gsi_info),0).name
      "MARKETS_TABLE_STATUS_VALID_AT_GSI" =  element(jsondecode(var.markets_gsi_info),1).name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_markets" {
  name = "/aws/lambda/${aws_lambda_function.lambda_markets.function_name}"

  retention_in_days = 14
  tags = local.common_tags
}

data "archive_file" "lambda_markets" {
  type = "zip"

  source_dir  = "${path.module}/api/markets"
  output_path = "${path.module}/templates/markets.zip"
}

resource "aws_s3_object" "lambda_markets" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "markets.zip"
  source = data.archive_file.lambda_markets.output_path

  etag = filemd5(data.archive_file.lambda_markets.output_path)
}

# ---------------------------------------------- #
#  TEST EVENT  Example
# ---------------------------------------------- #


# locals {
#   markets_test_event = jsondecode(file("${path.module}/api/markets/event.json"))
# }


# resource "aws_lambda_invocation" "post_markets" {
#   depends_on = [aws_lambda_function.lambda_markets, aws_dynamodb_table.markets]
#   function_name = aws_lambda_function.lambda_markets.function_name
#   input         = jsonencode(local.markets_test_event[2])
# }

# resource "aws_lambda_invocation" "post_market" {
#   depends_on = [aws_lambda_function.lambda_markets, aws_dynamodb_table.markets]
#   function_name = aws_lambda_function.lambda_markets.function_name
#   input         = jsonencode(local.markets_test_event[5])
# }

# resource "aws_lambda_invocation" "query_markets" {
#   depends_on = [aws_lambda_function.lambda_markets, aws_dynamodb_table.markets]
#   function_name = aws_lambda_function.lambda_markets.function_name
#   input         = jsonencode(local.markets_test_event[0])
# }

# resource "aws_lambda_invocation" "scan_markets" {
#   depends_on = [aws_lambda_function.lambda_markets, aws_dynamodb_table.markets]
#   function_name = aws_lambda_function.lambda_markets.function_name
#   input         = jsonencode(local.markets_test_event[1])
# }


# resource "aws_lambda_invocation" "delete_markets" {
#   depends_on = [aws_lambda_function.lambda_markets, aws_dynamodb_table.markets]
#   function_name = aws_lambda_function.lambda_markets.function_name
#   input         = jsonencode(local.markets_test_event[3])
# }
# resource "aws_lambda_invocation" "get_market" {
#   depends_on = [aws_lambda_function.lambda_markets, aws_dynamodb_table.markets]
#   function_name = aws_lambda_function.lambda_markets.function_name
#   input         = jsonencode(local.markets_test_event[4])
# }

# resource "aws_lambda_invocation" "put_market" {
#   depends_on = [aws_lambda_function.lambda_markets, aws_dynamodb_table.markets]
#   function_name = aws_lambda_function.lambda_markets.function_name
#   input         = jsonencode(local.markets_test_event[6])
# }
# resource "aws_lambda_invocation" "delete_market" {
#   depends_on = [aws_lambda_function.lambda_markets, aws_dynamodb_table.markets]
#   function_name = aws_lambda_function.lambda_markets.function_name
#   input         = jsonencode(local.markets_test_event[7])
# }
# output "markets_test_markets_test_events_results" {
#   value = {
#     query_markets = aws_lambda_invocation.query_markets.result,
#     scan_markets = aws_lambda_invocation.scan_markets.result
#     post_markets = aws_lambda_invocation.post_markets.result
#     delete_markets = aws_lambda_invocation.delete_markets.result
#     get_market = aws_lambda_invocation.get_market.result
#     post_market = aws_lambda_invocation.post_market.result
#     put_market = aws_lambda_invocation.put_market.result
#     delete_market = aws_lambda_invocation.delete_market.result
#   }
# }
