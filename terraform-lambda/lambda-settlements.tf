

resource "aws_lambda_function" "lambda_settlements" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-settlements-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_settlements.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]
  source_code_hash = data.archive_file.lambda_settlements.output_base64sha256

  environment {
    variables = {
      "SETTLEMENTS_TABLE_NAME" = var.settlements_table_name
      "SETTLEMENTS_TABLE_ORDER_ID_VALID_AT_GSI" =  element(jsondecode(var.settlements_gsi_info),0).name
      # "SETTLEMENTS_TABLE_ORDER_ID_VALID_AT_GSI" =  element(tolist(aws_dynamodb_table.settlements.global_secondary_index), 0).name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_settlements" {
  name = "/aws/lambda/${aws_lambda_function.lambda_settlements.function_name}"

  retention_in_days = 14
  tags = local.common_tags
}

data "archive_file" "lambda_settlements" {
  type = "zip"

  source_dir  = "${path.module}/api/settlements"
  output_path = "${path.module}/templates/settlements.zip"
}

resource "aws_s3_object" "lambda_settlements" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "settlements.zip"
  source = data.archive_file.lambda_settlements.output_path

  etag = filemd5(data.archive_file.lambda_settlements.output_path)
}


# ---------------------------------------------- #
#  TEST EVENT  Example
# ---------------------------------------------- #


# locals {
#   settlements_test_event = jsondecode(file("${path.module}/api/settlements/event.json"))
# }


# resource "aws_lambda_invocation" "post_settlements" {
#   depends_on = [aws_lambda_function.lambda_settlements, aws_dynamodb_table.settlements]
#   function_name = aws_lambda_function.lambda_settlements.function_name
#   input         = jsonencode(local.settlements_test_event[2])
# }

# resource "aws_lambda_invocation" "post_settlement" {
#   depends_on = [aws_lambda_function.lambda_settlements, aws_dynamodb_table.settlements]
#   function_name = aws_lambda_function.lambda_settlements.function_name
#   input         = jsonencode(local.settlements_test_event[5])
# }

# resource "aws_lambda_invocation" "query_settlements" {
#   depends_on = [aws_lambda_function.lambda_settlements, aws_dynamodb_table.settlements]
#   function_name = aws_lambda_function.lambda_settlements.function_name
#   input         = jsonencode(local.settlements_test_event[0])
# }

# resource "aws_lambda_invocation" "scan_settlements" {
#   depends_on = [aws_lambda_function.lambda_settlements, aws_dynamodb_table.settlements]
#   function_name = aws_lambda_function.lambda_settlements.function_name
#   input         = jsonencode(local.settlements_test_event[1])
# }


# resource "aws_lambda_invocation" "delete_settlements" {
#   depends_on = [aws_lambda_function.lambda_settlements, aws_dynamodb_table.settlements]
#   function_name = aws_lambda_function.lambda_settlements.function_name
#   input         = jsonencode(local.settlements_test_event[3])
# }
# resource "aws_lambda_invocation" "get_settlement" {
#   depends_on = [aws_lambda_function.lambda_settlements, aws_dynamodb_table.settlements]
#   function_name = aws_lambda_function.lambda_settlements.function_name
#   input         = jsonencode(local.settlements_test_event[4])
# }

# resource "aws_lambda_invocation" "put_settlement" {
#   depends_on = [aws_lambda_function.lambda_settlements, aws_dynamodb_table.settlements]
#   function_name = aws_lambda_function.lambda_settlements.function_name
#   input         = jsonencode(local.settlements_test_event[6])
# }
# resource "aws_lambda_invocation" "delete_settlement" {
#   depends_on = [aws_lambda_function.lambda_settlements, aws_dynamodb_table.settlements]
#   function_name = aws_lambda_function.lambda_settlements.function_name
#   input         = jsonencode(local.settlements_test_event[7])
# }
# output "settlements_test_settlements_test_events_results" {
#   value = {
#     query_settlements = aws_lambda_invocation.query_settlements.result,
#     scan_settlements = aws_lambda_invocation.scan_settlements.result
#     post_settlements = aws_lambda_invocation.post_settlements.result
#     delete_settlements = aws_lambda_invocation.delete_settlements.result
#     get_settlement = aws_lambda_invocation.get_settlement.result
#     post_settlement = aws_lambda_invocation.post_settlement.result
#     put_settlement = aws_lambda_invocation.put_settlement.result
#     delete_settlement = aws_lambda_invocation.delete_settlement.result
#   }
# }
