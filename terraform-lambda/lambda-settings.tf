

resource "aws_lambda_function" "lambda_settings" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-settings-api"

  s3_bucket = var.meta_data_bucket_name
  s3_key    = aws_s3_object.lambda_settings.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]
  source_code_hash = data.archive_file.lambda_settings.output_base64sha256

  environment {
    variables = {
      "SETTINGS_TABLE_NAME" = var.settings_table_name
       "SETTINGS_TABLE_DEVICE_ID_VALID_AT_GSI" = element(jsondecode(var.settings_gsi_info),0).name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_settings" {
  name = "/aws/lambda/${aws_lambda_function.lambda_settings.function_name}"

  retention_in_days = 14
  tags = local.common_tags
}

data "archive_file" "lambda_settings" {
  type = "zip"

  source_dir  = "${path.module}/api/settings"
  output_path = "${path.module}/templates/settings.zip"
}

resource "aws_s3_object" "lambda_settings" {
  bucket = var.meta_data_bucket_name

  key    = "settings/settings.zip"
  source = data.archive_file.lambda_settings.output_path

  etag = filemd5(data.archive_file.lambda_settings.output_path)
}

# Log stream
resource "aws_cloudwatch_log_stream" "lambda_settings" {
  name = "/aws/lambda_logstream/${aws_lambda_function.lambda_settings.function_name}"
  log_group_name = aws_cloudwatch_log_group.lambda_settings.name
}


resource "aws_lambda_permission" "lambda_settings" {
  statement_id  = "AllowExecutionFromCloudWatchLogs"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_settings.function_name

  principal = "logs.${var.aws_region}.amazonaws.com"

  source_arn = aws_cloudwatch_log_group.lambda_settings.arn

}

# ---------------------------------------------- #
#  TEST EVENT  Example
# ---------------------------------------------- #


# locals {
#   settings_test_event = jsondecode(file("${path.module}/api/settings/event.json"))
# }


# resource "aws_lambda_invocation" "post_settings" {
#   depends_on = [aws_lambda_function.lambda_settings, aws_dynamodb_table.settings]
#   function_name = aws_lambda_function.lambda_settings.function_name
#   input         = jsonencode(local.settings_test_event[2])
# }

# resource "aws_lambda_invocation" "post_setting" {
#   depends_on = [aws_lambda_function.lambda_settings, aws_dynamodb_table.settings]
#   function_name = aws_lambda_function.lambda_settings.function_name
#   input         = jsonencode(local.settings_test_event[5])
# }

# resource "aws_lambda_invocation" "query_settings" {
#   depends_on = [aws_lambda_function.lambda_settings, aws_dynamodb_table.settings]
#   function_name = aws_lambda_function.lambda_settings.function_name
#   input         = jsonencode(local.settings_test_event[0])
# }

# resource "aws_lambda_invocation" "scan_settings" {
#   depends_on = [aws_lambda_function.lambda_settings, aws_dynamodb_table.settings]
#   function_name = aws_lambda_function.lambda_settings.function_name
#   input         = jsonencode(local.settings_test_event[1])
# }


# resource "aws_lambda_invocation" "delete_settings" {
#   depends_on = [aws_lambda_function.lambda_settings, aws_dynamodb_table.settings]
#   function_name = aws_lambda_function.lambda_settings.function_name
#   input         = jsonencode(local.settings_test_event[3])
# }
# resource "aws_lambda_invocation" "get_setting" {
#   depends_on = [aws_lambda_function.lambda_settings, aws_dynamodb_table.settings]
#   function_name = aws_lambda_function.lambda_settings.function_name
#   input         = jsonencode(local.settings_test_event[4])
# }

# resource "aws_lambda_invocation" "put_setting" {
#   depends_on = [aws_lambda_function.lambda_settings, aws_dynamodb_table.settings]
#   function_name = aws_lambda_function.lambda_settings.function_name
#   input         = jsonencode(local.settings_test_event[6])
# }
# resource "aws_lambda_invocation" "delete_setting" {
#   depends_on = [aws_lambda_function.lambda_settings, aws_dynamodb_table.settings]
#   function_name = aws_lambda_function.lambda_settings.function_name
#   input         = jsonencode(local.settings_test_event[7])
# }
# output "settings_test_settings_test_events_results" {
#   value = {
#     query_settings = aws_lambda_invocation.query_settings.result,
#     scan_settings = aws_lambda_invocation.scan_settings.result
#     post_settings = aws_lambda_invocation.post_settings.result
#     delete_settings = aws_lambda_invocation.delete_settings.result
#     get_setting = aws_lambda_invocation.get_setting.result
#     post_setting = aws_lambda_invocation.post_setting.result
#     put_setting = aws_lambda_invocation.put_setting.result
#     delete_setting = aws_lambda_invocation.delete_setting.result
#   }
# }
