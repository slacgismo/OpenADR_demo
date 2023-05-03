

resource "aws_lambda_function" "lambda_weather" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-weather-api"

  s3_bucket = var.meta_data_bucket_name
  s3_key    = aws_s3_object.lambda_weather.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"
 layers        = [aws_lambda_layer_version.shared_layers.arn]
  source_code_hash = data.archive_file.lambda_weather.output_base64sha256

  environment {
    variables = {
      "WEATHER_TABLE_NAME" = var.weather_table_name
      "WEATHER_TABLE_ZIP_CODE_VALID_AT_GSI" =element(jsondecode(var.weather_gsi_info),0).name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_weather" {
  name = "/aws/lambda/${aws_lambda_function.lambda_weather.function_name}"

  retention_in_days = 14
  tags = local.common_tags
}

data "archive_file" "lambda_weather" {
  type = "zip"

  source_dir  = "../api/weather"
  output_path = "${path.module}/templates/weather.zip"
}

resource "aws_s3_object" "lambda_weather" {
  bucket =var.meta_data_bucket_name

  key    = "weeather/weather.zip"
  source = data.archive_file.lambda_weather.output_path

  etag = filemd5(data.archive_file.lambda_weather.output_path)
}

# Log stream
resource "aws_cloudwatch_log_stream" "lambda_weather" {
  name = "/aws/lambda_logstream/${aws_lambda_function.lambda_weather.function_name}"
  log_group_name = aws_cloudwatch_log_group.lambda_weather.name
}


resource "aws_lambda_permission" "lambda_weather" {
  statement_id  = "AllowExecutionFromCloudWatchLogs"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_weather.function_name

  principal = "logs.${var.aws_region}.amazonaws.com"

  source_arn = aws_cloudwatch_log_group.lambda_weather.arn

}

# ---------------------------------------------- #
#  TEST EVENT  Example
# ---------------------------------------------- #


# locals {
#   weathers_test_event = jsondecode(file("${path.module}/api/weather/event.json"))
# }


# resource "aws_lambda_invocation" "post_weathers" {
#   depends_on = [aws_lambda_function.lambda_weather, aws_dynamodb_table.weather]
#   function_name = aws_lambda_function.lambda_weather.function_name
#   input         = jsonencode(local.weathers_test_event[2])
# }

# resource "aws_lambda_invocation" "post_weather" {
#   depends_on = [aws_lambda_function.lambda_weather, aws_dynamodb_table.weather]
#   function_name = aws_lambda_function.lambda_weather.function_name
#   input         = jsonencode(local.weathers_test_event[5])
# }

# resource "aws_lambda_invocation" "query_weathers" {
#   depends_on = [aws_lambda_function.lambda_weather, aws_dynamodb_table.weather]
#   function_name = aws_lambda_function.lambda_weather.function_name
#   input         = jsonencode(local.weathers_test_event[0])
# }

# resource "aws_lambda_invocation" "scan_weathers" {
#   depends_on = [aws_lambda_function.lambda_weather, aws_dynamodb_table.weather]
#   function_name = aws_lambda_function.lambda_weather.function_name
#   input         = jsonencode(local.weathers_test_event[1])
# }


# resource "aws_lambda_invocation" "delete_weathers" {
#   depends_on = [aws_lambda_function.lambda_weather, aws_dynamodb_table.weather]
#   function_name = aws_lambda_function.lambda_weather.function_name
#   input         = jsonencode(local.weathers_test_event[3])
# }
# resource "aws_lambda_invocation" "get_weather" {
#   depends_on = [aws_lambda_function.lambda_weather, aws_dynamodb_table.weather]
#   function_name = aws_lambda_function.lambda_weather.function_name
#   input         = jsonencode(local.weathers_test_event[4])
# }

# resource "aws_lambda_invocation" "put_weather" {
#   depends_on = [aws_lambda_function.lambda_weather, aws_dynamodb_table.weather]
#   function_name = aws_lambda_function.lambda_weather.function_name
#   input         = jsonencode(local.weathers_test_event[6])
# }
# resource "aws_lambda_invocation" "delete_weather" {
#   depends_on = [aws_lambda_function.lambda_weather, aws_dynamodb_table.weather]
#   function_name = aws_lambda_function.lambda_weather.function_name
#   input         = jsonencode(local.weathers_test_event[7])
# }
# output "weathers_test_weathers_test_events_results" {
#   value = {
#     query_weathers = aws_lambda_invocation.query_weathers.result,
#     scan_weathers = aws_lambda_invocation.scan_weathers.result
#     post_weathers = aws_lambda_invocation.post_weathers.result
#     delete_weathers = aws_lambda_invocation.delete_weathers.result
#     get_weather = aws_lambda_invocation.get_weather.result
#     post_weather = aws_lambda_invocation.post_weather.result
#     put_weather = aws_lambda_invocation.put_weather.result
#     delete_weather = aws_lambda_invocation.delete_weather.result
#   }
# }
