
resource "aws_lambda_function" "lambda_meters" {
  # function_name = "battery_api"
  function_name = "${var.prefix}-${var.client}-${var.environment}-meters-api"

  s3_bucket = var.meta_data_bucket_name
  s3_key    = aws_s3_object.lambda_meters.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]
  source_code_hash = data.archive_file.lambda_meters.output_base64sha256
  environment {
    variables = {
      "METERS_TABLE_NAME" = var.meters_table_name
      "METERS_TABLE_RESOURCE_ID_DEVICE_ID_GSI" =  element(jsondecode(var.meters_gsi_info),0).name
      "METERS_TABLE_METER_STATUS_VALID_AT_GSI" =  element(jsondecode(var.meters_gsi_info),1).name
      # "READINGS_TIMESTREAM_TABLE_NAME" = aws_timestreamwrite_table.readings.table_name
      # "TIMESTREAM_DB_NAME" = aws_timestreamwrite_database.measurements.database_name
    }
  }
  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_meters" {
  name = "/aws/lambda/${aws_lambda_function.lambda_meters.function_name}"

  retention_in_days = 14
  tags = local.common_tags
}

data "archive_file" "lambda_meters" {
  type = "zip"

  source_dir  = "${path.module}/api/meters"
  output_path = "${path.module}/templates/meters.zip"
}

resource "aws_s3_object" "lambda_meters" {
  bucket = var.meta_data_bucket_name

  key    = "meters/meters.zip"
  source = data.archive_file.lambda_meters.output_path

  etag = filemd5(data.archive_file.lambda_meters.output_path)
}

# Log stream
resource "aws_cloudwatch_log_stream" "lambda_meters" {
  name = "/aws/lambda_logstream/${aws_lambda_function.lambda_meters.function_name}"
  log_group_name = aws_cloudwatch_log_group.lambda_meters.name
}


resource "aws_lambda_permission" "lambda_meters" {
  statement_id  = "AllowExecutionFromCloudWatchLogs"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_meters.function_name

  principal = "logs.${var.aws_region}.amazonaws.com"

  source_arn = aws_cloudwatch_log_group.lambda_meters.arn

}


# ---------------------------------------------- #
#  TEST EVENT  Example
# ---------------------------------------------- #


locals {
  meters_test_event = jsondecode(file("${path.module}/api/meters/event.json"))
}


resource "aws_lambda_invocation" "post_meters" {
  depends_on = [aws_lambda_function.lambda_meters,]
  function_name = aws_lambda_function.lambda_meters.function_name
  input         = jsonencode(local.meters_test_event[2])
}

resource "aws_lambda_invocation" "post_meter" {

  depends_on = [aws_lambda_function.lambda_meters]
   function_name = aws_lambda_function.lambda_meters.function_name
  input         = jsonencode(local.meters_test_event[5])
}

resource "aws_lambda_invocation" "query_meters" {
  depends_on = [aws_lambda_function.lambda_meters]
  function_name = aws_lambda_function.lambda_meters.function_name
  input         = jsonencode(local.meters_test_event[0])
}

resource "aws_lambda_invocation" "scan_meters" {
  depends_on = [aws_lambda_function.lambda_meters]
  function_name = aws_lambda_function.lambda_meters.function_name
  input         = jsonencode(local.meters_test_event[1])
}


resource "aws_lambda_invocation" "delete_meters" {
  function_name = aws_lambda_function.lambda_meters.function_name
  input         = jsonencode(local.meters_test_event[3])
}
resource "aws_lambda_invocation" "get_meter" {
  depends_on = [aws_lambda_function.lambda_meters]
  function_name = aws_lambda_function.lambda_meters.function_name
  input         = jsonencode(local.meters_test_event[4])
}

resource "aws_lambda_invocation" "put_meter" {
  function_name = aws_lambda_function.lambda_meters.function_name
  input         = jsonencode(local.meters_test_event[6])
}
resource "aws_lambda_invocation" "delete_meter" {
  depends_on = [aws_lambda_function.lambda_meters]
  function_name = aws_lambda_function.lambda_meters.function_name
  input         = jsonencode(local.meters_test_event[7])
}
output "meters_test_meters_test_events_results" {
  value = {
    query_meters = aws_lambda_invocation.query_meters.result,
    scan_meters = aws_lambda_invocation.scan_meters.result
    post_meters = aws_lambda_invocation.post_meters.result
    delete_meters = aws_lambda_invocation.delete_meters.result
    get_meter = aws_lambda_invocation.get_meter.result
    post_meter = aws_lambda_invocation.post_meter.result
    put_meter = aws_lambda_invocation.put_meter.result
    delete_meter = aws_lambda_invocation.delete_meter.result
  }
}
