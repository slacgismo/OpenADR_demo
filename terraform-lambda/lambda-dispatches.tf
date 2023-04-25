

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
        "DISPATCHED_TABLE_NAME" = aws_dynamodb_table.dispatches.name
        "DISPATCHED_TABLE_ORDER_ID_VALID_AT_GSI" =  element(tolist(aws_dynamodb_table.dispatches.global_secondary_index), 0).name
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