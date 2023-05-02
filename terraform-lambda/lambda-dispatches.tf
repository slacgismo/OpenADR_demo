

resource "aws_lambda_function" "dispatches" {
  # function_name = "participated_vens"
  function_name = "${var.prefix}-${var.client}-${var.environment}-dispatch-api"
  s3_bucket     = aws_s3_bucket.lambda_bucket.id
  s3_key        = aws_s3_object.dispatch_vens.key
  runtime       = "python3.9"
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]
  timeout       = 60
  memory_size   = 128
 
  source_code_hash = data.archive_file.dispatch_vens.output_base64sha256
  environment {
      variables = {
        "DISPATCHED_TABLE_NAME" = var.dispatches_table_name
        "DISPATCHED_TABLE_ORDER_ID_VALID_AT_GSI" =  element(jsondecode(var.dispatches_gsi_info),0).name
          # "DISPATCHES_TIMESTREAM_TABLE_NAME" = aws_timestreamwrite_table.dispatches.table_name
          # "TIMESTREAM_DB_NAME"= aws_timestreamwrite_database.measurements.database_name
    }
  }
  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "participated_vens" {
  name = "/aws/lambda/${aws_lambda_function.dispatches.function_name}"

  retention_in_days = 14
  tags = local.common_tags
}

data "archive_file" "dispatch_vens" {
  type = "zip"

  source_dir  = "${path.module}/api/dispatches"
  output_path = "${path.module}/templates/dispatches.zip"
}

resource "aws_s3_object" "dispatch_vens" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "dispatches.zip"
  source = data.archive_file.dispatch_vens.output_path

  etag = filemd5(data.archive_file.dispatch_vens.output_path)
}


# ---------------------------------------------- #
#  TEST EVENT  Example
# ---------------------------------------------- #


# locals {
#   dispatches_test_event = jsondecode(file("${path.module}/api/dispatches/event.json"))
# }


# resource "aws_lambda_invocation" "post_dispatches" {
#   function_name = aws_lambda_function.dispatches.function_name
#   input         = jsonencode(local.dispatches_test_event[2])
# }

# resource "aws_lambda_invocation" "post_dispatch" {
#   function_name = aws_lambda_function.dispatches.function_name
#   input         = jsonencode(local.dispatches_test_event[5])
# }

# resource "aws_lambda_invocation" "query_dispatches" {
#   function_name = aws_lambda_function.dispatches.function_name
#   input         = jsonencode(local.dispatches_test_event[0])
# }

# resource "aws_lambda_invocation" "scan_dispatches" {
#   function_name = aws_lambda_function.dispatches.function_name
#   input         = jsonencode(local.dispatches_test_event[1])
# }


# resource "aws_lambda_invocation" "delete_dispatches" {
#   function_name = aws_lambda_function.dispatches.function_name
#   input         = jsonencode(local.dispatches_test_event[3])
# }
# resource "aws_lambda_invocation" "get_dispatch" {
#   function_name = aws_lambda_function.dispatches.function_name
#   input         = jsonencode(local.dispatches_test_event[4])
# }

# resource "aws_lambda_invocation" "put_dispatch" {
#   function_name = aws_lambda_function.dispatches.function_name
#   input         = jsonencode(local.dispatches_test_event[6])
# }
# resource "aws_lambda_invocation" "delete_dispatch" {
#   function_name = aws_lambda_function.dispatches.function_name
#   input         = jsonencode(local.dispatches_test_event[7])
# }
# output "dispatches_test_dispatches_test_events_results" {
#   value = {
#     query_dispatches = aws_lambda_invocation.query_dispatches.result,
#     scan_dispatches = aws_lambda_invocation.scan_dispatches.result
#     post_dispatches = aws_lambda_invocation.post_dispatches.result
#     delete_dispatches = aws_lambda_invocation.delete_dispatches.result
#     get_dispatch = aws_lambda_invocation.get_dispatch.result
#     post_dispatch = aws_lambda_invocation.post_dispatch.result
#     put_dispatch = aws_lambda_invocation.put_dispatch.result
#     delete_dispatch = aws_lambda_invocation.delete_dispatch.result
#   }
# }
