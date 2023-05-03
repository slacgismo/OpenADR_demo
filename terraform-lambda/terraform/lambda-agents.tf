

# ---------------------------------------------- #
# ------  Lambda Function for Agents API  ------ #
#   "GET /db/agents/{get_items_action}"
#   "PUT /db/agents"
#   "DELETE /db/agents"
# ---------------------------------------------- #
#   "GET /db/agent/{agent_id}"
#   "PUT /db/agent/{agent_id}"
#   "DELETE /db/agent/{agent_id}"
# ---------------------------------------------- #


resource "aws_lambda_function" "lambda_agents" {
  function_name = "${var.prefix}-${var.client}-${var.environment}-agents-api"

  s3_bucket = var.meta_data_bucket_name
  s3_key    = aws_s3_object.lambda_agents.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]

  source_code_hash = data.archive_file.lambda_agents.output_base64sha256

  environment {
    variables = {
      "AGENTS_TABLE_NAME" = var.agents_table_name
      "AGENTS_TABLE_RESOURCE_ID_VALID_AT_GSI" =  element( jsondecode(var.agents_gsi_info),0).name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}


# ---------------------------------------------- #
#  Log Group for Lambda Function for Agents API  #
# ---------------------------------------------- #
resource "aws_cloudwatch_log_group" "lambda_agents" {
  name = "/aws/lambda/${aws_lambda_function.lambda_agents.function_name}"

  retention_in_days = 14
  tags = local.common_tags
}

# ---------------------------------------------- #
#  Archieve file  #
# ---------------------------------------------- #
data "archive_file" "lambda_agents" {
  type = "zip"

  source_dir  = "../api/agents"
  output_path = "${path.module}/templates/agents.zip"
}

resource "aws_s3_object" "lambda_agents" {
  bucket = var.meta_data_bucket_name
  key    = "agents/agents.zip"
  source = data.archive_file.lambda_agents.output_path

  etag = filemd5(data.archive_file.lambda_agents.output_path)
}

# Log stream
resource "aws_cloudwatch_log_stream" "lambda_agents" {
  name = "/aws/lambda_logstream/${aws_lambda_function.lambda_agents.function_name}"
  log_group_name = aws_cloudwatch_log_group.lambda_agents.name
}


resource "aws_lambda_permission" "lambda_agents" {
  statement_id  = "AllowExecutionFromCloudWatchLogs"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_agents.function_name

  principal = "logs.${var.aws_region}.amazonaws.com"

  source_arn = aws_cloudwatch_log_group.lambda_agents.arn

}
# ---------------------------------------------- #
#  TEST EVENT  Example
# ---------------------------------------------- #


# locals {
#   agents_test_event = jsondecode(file("${path.module}/api/agents/event.json"))
# }


# resource "aws_lambda_invocation" "post_agents" {
#   depends_on = [aws_lambda_function.lambda_agents, aws_dynamodb_table.agents]
#   function_name = aws_lambda_function.lambda_agents.function_name
#   input         = jsonencode(local.agents_test_event[2])
# }

# resource "aws_lambda_invocation" "post_agent" {
#   depends_on = [aws_lambda_function.lambda_agents,aws_dynamodb_table.agents]
#   function_name = aws_lambda_function.lambda_agents.function_name
#   input         = jsonencode(local.agents_test_event[5])
# }

# resource "aws_lambda_invocation" "query_agents" {
#   depends_on = [aws_lambda_function.lambda_agents,aws_dynamodb_table.agents]
#   function_name = aws_lambda_function.lambda_agents.function_name
#   input         = jsonencode(local.agents_test_event[0])
# }

# resource "aws_lambda_invocation" "scan_agents" {
#   depends_on = [aws_lambda_function.lambda_agents,aws_dynamodb_table.agents]
#   function_name = aws_lambda_function.lambda_agents.function_name
#   input         = jsonencode(local.agents_test_event[1])
# }


# resource "aws_lambda_invocation" "delete_agents" {
#   depends_on = [aws_lambda_function.lambda_agents,aws_dynamodb_table.agents]
#   function_name = aws_lambda_function.lambda_agents.function_name
#   input         = jsonencode(local.agents_test_event[3])
# }
# resource "aws_lambda_invocation" "get_agent" {
#   depends_on = [aws_lambda_function.lambda_agents,aws_dynamodb_table.agents]
#   function_name = aws_lambda_function.lambda_agents.function_name
#   input         = jsonencode(local.agents_test_event[4])
# }

# resource "aws_lambda_invocation" "put_agent" {
#   depends_on = [aws_lambda_function.lambda_agents,aws_dynamodb_table.agents]
#   function_name = aws_lambda_function.lambda_agents.function_name
#   input         = jsonencode(local.agents_test_event[6])
# }
# resource "aws_lambda_invocation" "delete_agent" {
#   depends_on = [aws_lambda_function.lambda_agents]
#   function_name = aws_lambda_function.lambda_agents.function_name
#   input         = jsonencode(local.agents_test_event[7])
# }
# output "agents_test_agents_test_events_results" {
#   value = {
#     query_agents = aws_lambda_invocation.query_agents.result,
#     scan_agents = aws_lambda_invocation.scan_agents.result
#     post_agents = aws_lambda_invocation.post_agents.result
#     delete_agents = aws_lambda_invocation.delete_agents.result
#     get_agent = aws_lambda_invocation.get_agent.result
#     post_agent = aws_lambda_invocation.post_agent.result
#     put_agent = aws_lambda_invocation.put_agent.result
#     delete_agent = aws_lambda_invocation.delete_agent.result
#   }
# }