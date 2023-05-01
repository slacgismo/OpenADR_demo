

resource "aws_lambda_function" "lambda_resources" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-resources-api"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_resources.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]
  source_code_hash = data.archive_file.lambda_resources.output_base64sha256

  environment {
    variables = {
      "RESOURCES_TABLE_NAME" = aws_dynamodb_table.resources.name
      "RESOURCES_TABLE_STATUS_VALID_AT_GSI" = element(tolist(aws_dynamodb_table.resources.global_secondary_index), 0).name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_resources" {
  name = "/aws/lambda/${aws_lambda_function.lambda_resources.function_name}"

  retention_in_days = 14
  tags = local.common_tags
}

data "archive_file" "lambda_resources" {
  type = "zip"

  source_dir  = "${path.module}/api/resources"
  output_path = "${path.module}/templates/resources.zip"
}

resource "aws_s3_object" "lambda_resources" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "resources.zip"
  source = data.archive_file.lambda_resources.output_path

  etag = filemd5(data.archive_file.lambda_resources.output_path)
}


# ---------------------------------------------- #
#  TEST EVENT  Example
# ---------------------------------------------- #


locals {
  resources_test_event = jsondecode(file("${path.module}/api/resources/event.json"))
}


resource "aws_lambda_invocation" "post_resources" {
  depends_on = [aws_lambda_function.lambda_resources, aws_dynamodb_table.resources]
  function_name = aws_lambda_function.lambda_resources.function_name
  input         = jsonencode(local.resources_test_event[2])
}

resource "aws_lambda_invocation" "post_resource" {
  depends_on = [aws_lambda_function.lambda_resources, aws_dynamodb_table.resources]
  function_name = aws_lambda_function.lambda_resources.function_name
  input         = jsonencode(local.resources_test_event[5])
}

resource "aws_lambda_invocation" "query_resources" {
  depends_on = [aws_lambda_function.lambda_resources, aws_dynamodb_table.resources]
  function_name = aws_lambda_function.lambda_resources.function_name
  input         = jsonencode(local.resources_test_event[0])
}

resource "aws_lambda_invocation" "scan_resources" {
  depends_on = [aws_lambda_function.lambda_resources, aws_dynamodb_table.resources]
  function_name = aws_lambda_function.lambda_resources.function_name
  input         = jsonencode(local.resources_test_event[1])
}


resource "aws_lambda_invocation" "delete_resources" {
  depends_on = [aws_lambda_function.lambda_resources, aws_dynamodb_table.resources]
  function_name = aws_lambda_function.lambda_resources.function_name
  input         = jsonencode(local.resources_test_event[3])
}
resource "aws_lambda_invocation" "get_resource" {
  depends_on = [aws_lambda_function.lambda_resources, aws_dynamodb_table.resources]
  function_name = aws_lambda_function.lambda_resources.function_name
  input         = jsonencode(local.resources_test_event[4])
}

resource "aws_lambda_invocation" "put_resource" {
  depends_on = [aws_lambda_function.lambda_resources, aws_dynamodb_table.resources]
  function_name = aws_lambda_function.lambda_resources.function_name
  input         = jsonencode(local.resources_test_event[6])
}
resource "aws_lambda_invocation" "delete_resource" {
  depends_on = [aws_lambda_function.lambda_resources, aws_dynamodb_table.resources]
  function_name = aws_lambda_function.lambda_resources.function_name
  input         = jsonencode(local.resources_test_event[7])
}
output "resources_test_resources_test_events_results" {
  value = {
    query_resources = aws_lambda_invocation.query_resources.result,
    scan_resources = aws_lambda_invocation.scan_resources.result
    post_resources = aws_lambda_invocation.post_resources.result
    delete_resources = aws_lambda_invocation.delete_resources.result
    get_resource = aws_lambda_invocation.get_resource.result
    post_resource = aws_lambda_invocation.post_resource.result
    put_resource = aws_lambda_invocation.put_resource.result
    delete_resource = aws_lambda_invocation.delete_resource.result
  }
}
