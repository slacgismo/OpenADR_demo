


resource "aws_lambda_function" "lambda_readings" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-readings-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_readings.key
  runtime   = "python3.9"
    timeout       = 60
  memory_size   = 128
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]
  source_code_hash = data.archive_file.lambda_readings.output_base64sha256

  environment {
    variables = {
      "READINGS_TABLE_NAME" = aws_dynamodb_table.readings.name
      "READINGS_TABLE_METER_ID_GSI" = element(tolist(aws_dynamodb_table.readings.global_secondary_index), 0).name
      "READINGS_TABLE_METER_ID_VALID_AT_GSI" = element(tolist(aws_dynamodb_table.readings.global_secondary_index), 1).name
      # "ORDERS_TIMESTEAM_TABLE_NAME" = aws_timestreamwrite_table.orders.table_name
      # "TIMESTREAM_DB_NAME" = aws_timestreamwrite_database.measurements.database_name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_readings" {
  name = "/aws/lambda/${aws_lambda_function.lambda_readings.function_name}"

  retention_in_days = 14
  tags = local.common_tags
}

data "archive_file" "lambda_readings" {
  type = "zip"

  source_dir  = "${path.module}/api/readings"
  output_path = "${path.module}/templates/readings.zip"
}

resource "aws_s3_object" "lambda_readings" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "readings.zip"
  source = data.archive_file.lambda_readings.output_path

  etag = filemd5(data.archive_file.lambda_orders.output_path)
}

# ---------------------------------------------- #
#  TEST EVENT  Example
# ---------------------------------------------- #


# locals {
#   readings_test_event = jsondecode(file("${path.module}/api/readings/event.json"))
# }


# resource "aws_lambda_invocation" "post_readings" {
#   depends_on = [aws_lambda_function.lambda_readings, aws_dynamodb_table.readings]
#   function_name = aws_lambda_function.lambda_readings.function_name
#   input         = jsonencode(local.readings_test_event[2])
# }

# resource "aws_lambda_invocation" "post_reading" {
#   depends_on = [aws_lambda_function.lambda_readings, aws_dynamodb_table.readings]
#   function_name = aws_lambda_function.lambda_readings.function_name
#   input         = jsonencode(local.readings_test_event[5])
# }

# resource "aws_lambda_invocation" "query_readings" {
#   depends_on = [aws_lambda_function.lambda_readings, aws_dynamodb_table.readings]
#   function_name = aws_lambda_function.lambda_readings.function_name
#   input         = jsonencode(local.readings_test_event[0])
# }

# resource "aws_lambda_invocation" "scan_readings" {
#   depends_on = [aws_lambda_function.lambda_readings, aws_dynamodb_table.readings]
#   function_name = aws_lambda_function.lambda_readings.function_name
#   input         = jsonencode(local.readings_test_event[1])
# }


# resource "aws_lambda_invocation" "delete_readings" {
#   depends_on = [aws_lambda_function.lambda_readings, aws_dynamodb_table.readings]
#   function_name = aws_lambda_function.lambda_readings.function_name
#   input         = jsonencode(local.readings_test_event[3])
# }
# resource "aws_lambda_invocation" "get_reading" {
#   depends_on = [aws_lambda_function.lambda_readings, aws_dynamodb_table.readings]
#   function_name = aws_lambda_function.lambda_readings.function_name
#   input         = jsonencode(local.readings_test_event[4])
# }

# resource "aws_lambda_invocation" "put_reading" {
#   depends_on = [aws_lambda_function.lambda_readings, aws_dynamodb_table.readings]
#   function_name = aws_lambda_function.lambda_readings.function_name
#   input         = jsonencode(local.readings_test_event[6])
# }
# resource "aws_lambda_invocation" "delete_reading" {
#   depends_on = [aws_lambda_function.lambda_readings, aws_dynamodb_table.readings]
#   function_name = aws_lambda_function.lambda_readings.function_name
#   input         = jsonencode(local.readings_test_event[7])
# }
# output "readings_test_readings_test_events_results" {
#   value = {
#     query_readings = aws_lambda_invocation.query_readings.result,
#     scan_readings = aws_lambda_invocation.scan_readings.result
#     post_readings = aws_lambda_invocation.post_readings.result
#     delete_readings = aws_lambda_invocation.delete_readings.result
#     get_reading = aws_lambda_invocation.get_reading.result
#     post_reading = aws_lambda_invocation.post_reading.result
#     put_reading = aws_lambda_invocation.put_reading.result
#     delete_reading = aws_lambda_invocation.delete_reading.result
#   }
# }
