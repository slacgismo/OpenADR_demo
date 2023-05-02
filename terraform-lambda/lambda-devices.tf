



# ---------------------------------------------- #
# ------  Lambda Function for Devices API  ------ #
# "GET /db/devices" Get a list of devices
# Get /db/devices/{<device_id>}, Get a device by id readings.
# Put /db/device/<device_id>
# DELETE /db/device/<device_id>
# ---------------------------------------------- #

resource "aws_lambda_function" "lambda_devices" {

  function_name = "${var.prefix}-${var.client}-${var.environment}-devices-api"
  s3_bucket     = var.meta_data_bucket_name
  s3_key        = aws_s3_object.lambda_devices.key
  runtime       = "python3.9"
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]
  timeout       = 60
  memory_size   = 128
 
  source_code_hash = data.archive_file.lambda_devices.output_base64sha256
  environment {
      variables = {
          "DEVICES_TABLE_NAME" = var.devices_table_name
          "DEVICES_TABLE_AGENT_ID_VALID_AT_GSI" =  element(jsondecode(var.devices_gsi_info),0).name
          "DEVICES_TABLE_STATUS_VALID_AT_GSI" = element(jsondecode(var.devices_gsi_info),1).name
      }
  }


  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}
# ---------------------------------------------- #
# DEVICES and DEVICE API LAMBDA SHARE RESOURCES
# ---------------------------------------------- #
resource "aws_cloudwatch_log_group" "lambda_devices" {
  name = "/aws/lambda/${aws_lambda_function.lambda_devices.function_name}"

  retention_in_days = 14
  tags = local.common_tags
}

data "archive_file" "lambda_devices" {
  type = "zip"

  source_dir  = "${path.module}/api/devices"
  output_path = "${path.module}/templates/devices.zip"
}

resource "aws_s3_object" "lambda_devices" {
  bucket = var.meta_data_bucket_name

  key    = "devices/devices.zip"
  source = data.archive_file.lambda_devices.output_path

  etag = filemd5(data.archive_file.lambda_devices.output_path)
}


# Log stream
resource "aws_cloudwatch_log_stream" "lambda_devices" {
  name = "/aws/lambda_logstream/${aws_lambda_function.lambda_devices.function_name}"
  log_group_name = aws_cloudwatch_log_group.lambda_devices.name
}


resource "aws_lambda_permission" "lambda_devices" {
  statement_id  = "AllowExecutionFromCloudWatchLogs"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_devices.function_name

  principal = "logs.${var.aws_region}.amazonaws.com"

  source_arn = aws_cloudwatch_log_group.lambda_devices.arn

}
# ---------------------------------------------- #
#  TEST EVENT  Example
# ---------------------------------------------- #


# locals {
#   devices_test_event = jsondecode(file("${path.module}/api/devices/event.json"))
# }


# resource "aws_lambda_invocation" "post_devices" {
#   function_name = aws_lambda_function.lambda_devices.function_name
#   input         = jsonencode(local.devices_test_event[2])
# }

# resource "aws_lambda_invocation" "post_device" {
#   function_name = aws_lambda_function.lambda_devices.function_name
#   input         = jsonencode(local.devices_test_event[5])
# }

# resource "aws_lambda_invocation" "query_devices" {
#   function_name = aws_lambda_function.lambda_devices.function_name
#   input         = jsonencode(local.devices_test_event[0])
# }

# resource "aws_lambda_invocation" "scan_devices" {
#   function_name = aws_lambda_function.lambda_devices.function_name
#   input         = jsonencode(local.devices_test_event[1])
# }


# resource "aws_lambda_invocation" "delete_devices" {
#   function_name = aws_lambda_function.lambda_devices.function_name
#   input         = jsonencode(local.devices_test_event[3])
# }
# resource "aws_lambda_invocation" "get_device" {
#   function_name = aws_lambda_function.lambda_devices.function_name
#   input         = jsonencode(local.devices_test_event[4])
# }

# resource "aws_lambda_invocation" "put_device" {
#   function_name = aws_lambda_function.lambda_devices.function_name
#   input         = jsonencode(local.devices_test_event[6])
# }
# resource "aws_lambda_invocation" "delete_device" {
#   function_name = aws_lambda_function.lambda_devices.function_name
#   input         = jsonencode(local.devices_test_event[7])
# }
# output "devices_test_devices_test_events_results" {
#   value = {
#     query_devices = aws_lambda_invocation.query_devices.result,
#     scan_devices = aws_lambda_invocation.scan_devices.result
#     post_devices = aws_lambda_invocation.post_devices.result
#     delete_devices = aws_lambda_invocation.delete_devices.result
#     get_device = aws_lambda_invocation.get_device.result
#     post_device = aws_lambda_invocation.post_device.result
#     put_device = aws_lambda_invocation.put_device.result
#     delete_device = aws_lambda_invocation.delete_device.result
#   }
# }
