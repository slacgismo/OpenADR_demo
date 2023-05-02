


resource "aws_lambda_function" "lambda_orders" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-orders-api"

  s3_bucket =aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_orders.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]
  source_code_hash = data.archive_file.lambda_orders.output_base64sha256

  environment {
    variables = {
       "ORDERS_TABLE_NAME" = var.orders_table_name
        "ORDERS_TABLE_DEVICE_ID_ORDER_ID_GSI" = element(jsondecode(var.orders_gsi_info),0).name
        "ORDERS_TABLE_DEVICE_ID_VALID_AT_GSI" =  element(jsondecode(var.orders_gsi_info),1).name
      # "ORDERS_TIMESTEAM_TABLE_NAME" = aws_timestreamwrite_table.orders.table_name
      # "TIMESTREAM_DB_NAME" = aws_timestreamwrite_database.measurements.database_name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_orders" {
  name = "/aws/lambda/${aws_lambda_function.lambda_orders.function_name}"

  retention_in_days = 14
  tags = local.common_tags
}

data "archive_file" "lambda_orders" {
  type = "zip"

  source_dir  = "${path.module}/api/orders"
  output_path = "${path.module}/templates/orders.zip"
}

resource "aws_s3_object" "lambda_orders" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "orders.zip"
  source = data.archive_file.lambda_orders.output_path

  etag = filemd5(data.archive_file.lambda_orders.output_path)
}


# ---------------------------------------------- #
#  TEST EVENT  Example
# ---------------------------------------------- #


# locals {
#   orders_test_event = jsondecode(file("${path.module}/api/orders/event.json"))
# }


# resource "aws_lambda_invocation" "post_orders" {
#   depends_on = [aws_lambda_function.lambda_orders, aws_dynamodb_table.orders]
#   function_name = aws_lambda_function.lambda_orders.function_name
#   input         = jsonencode(local.orders_test_event[2])
# }

# resource "aws_lambda_invocation" "post_order" {
#   depends_on = [aws_lambda_function.lambda_orders, aws_dynamodb_table.orders]
#   function_name = aws_lambda_function.lambda_orders.function_name
#   input         = jsonencode(local.orders_test_event[5])
# }

# resource "aws_lambda_invocation" "query_orders" {
#   depends_on = [aws_lambda_function.lambda_orders, aws_dynamodb_table.orders]
#   function_name = aws_lambda_function.lambda_orders.function_name
#   input         = jsonencode(local.orders_test_event[0])
# }

# resource "aws_lambda_invocation" "scan_orders" {
#   depends_on = [aws_lambda_function.lambda_orders, aws_dynamodb_table.orders]
#   function_name = aws_lambda_function.lambda_orders.function_name
#   input         = jsonencode(local.orders_test_event[1])
# }


# resource "aws_lambda_invocation" "delete_orders" {
#   depends_on = [aws_lambda_function.lambda_orders, aws_dynamodb_table.orders]
#   function_name = aws_lambda_function.lambda_orders.function_name
#   input         = jsonencode(local.orders_test_event[3])
# }
# resource "aws_lambda_invocation" "get_order" {
#   depends_on = [aws_lambda_function.lambda_orders, aws_dynamodb_table.orders]
#   function_name = aws_lambda_function.lambda_orders.function_name
#   input         = jsonencode(local.orders_test_event[4])
# }

# resource "aws_lambda_invocation" "put_order" {
#   depends_on = [aws_lambda_function.lambda_orders, aws_dynamodb_table.orders]
#   function_name = aws_lambda_function.lambda_orders.function_name
#   input         = jsonencode(local.orders_test_event[6])
# }
# resource "aws_lambda_invocation" "delete_order" {
#   depends_on = [aws_lambda_function.lambda_orders, aws_dynamodb_table.orders]
#   function_name = aws_lambda_function.lambda_orders.function_name
#   input         = jsonencode(local.orders_test_event[7])
# }
# output "orders_test_orders_test_events_results" {
#   value = {
#     query_orders = aws_lambda_invocation.query_orders.result,
#     scan_orders = aws_lambda_invocation.scan_orders.result
#     post_orders = aws_lambda_invocation.post_orders.result
#     delete_orders = aws_lambda_invocation.delete_orders.result
#     get_order = aws_lambda_invocation.get_order.result
#     post_order = aws_lambda_invocation.post_order.result
#     put_order = aws_lambda_invocation.put_order.result
#     delete_order = aws_lambda_invocation.delete_order.result
#   }
# }
