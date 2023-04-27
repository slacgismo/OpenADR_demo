



# ---------------------------------------------- #
# ------  Lambda Function for Devices API  ------ #
# "GET /db/devices" Get a list of devices
# Get /db/devices/{<device_id>}, Get a device by id readings.
# Put /db/device/<device_id>
# DELETE /db/device/<device_id>
# ---------------------------------------------- #

resource "aws_lambda_function" "lamdba_devices" {

  function_name = "${var.prefix}-${var.client}-${var.environment}-devices-api"
  s3_bucket     = aws_s3_bucket.lambda_bucket.id
  s3_key        = aws_s3_object.lamdba_devices.key
  runtime       = "python3.9"
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]
  timeout       = 60
  memory_size   = 128
 
  source_code_hash = data.archive_file.lamdba_devices.output_base64sha256
  environment {
      variables = {
          "DEVICES_TABLE_NAME" = aws_dynamodb_table.devices.name
          "DEVICES_TABLE_AGENT_ID_VALID_AT_GSI" =  element(tolist(aws_dynamodb_table.devices.global_secondary_index), 0).name
          "DEVICES_TABLE_STATUS_VALID_AT_GSI" =  element(tolist(aws_dynamodb_table.devices.global_secondary_index), 1).name
    }
  }


  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}
# ---------------------------------------------- #
# DEVICES and DEVICE API LAMBDA SHARE RESOURCES
# ---------------------------------------------- #
resource "aws_cloudwatch_log_group" "lamdba_devices" {
  name = "/aws/lambda/${aws_lambda_function.lamdba_devices.function_name}"

  retention_in_days = 14
}

data "archive_file" "lamdba_devices" {
  type = "zip"

  source_dir  = "${path.module}/api/devices"
  output_path = "${path.module}/templates/devices.zip"
}

resource "aws_s3_object" "lamdba_devices" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "devices.zip"
  source = data.archive_file.lamdba_devices.output_path

  etag = filemd5(data.archive_file.lamdba_devices.output_path)
}

