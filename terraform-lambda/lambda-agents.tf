

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

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_agents.key
  runtime   = "python3.9"
  timeout       = 60
  memory_size   = 128
  handler = "function.handler"
  layers        = [aws_lambda_layer_version.shared_layers.arn]

  source_code_hash = data.archive_file.lambda_agents.output_base64sha256

  environment {
    variables = {
      "AGENTS_TABLE_NAME" = aws_dynamodb_table.agents.name
      "AGENTS_TABLE_RESOURCE_ID_VALID_AT_GSI" =  element(tolist(aws_dynamodb_table.agents.global_secondary_index), 0).name
    }
  }

  role = aws_iam_role.lambda_generic_exec_role.arn
  tags = local.common_tags
}


# ---------------------------------------------- #
#  Log Group for Lambda Function for Agents API  #
# ---------------------------------------------- #
# resource "aws_cloudwatch_log_group" "lambda_agents" {
#   name = "/aws/lambda/${aws_lambda_function.lambda_agents.function_name}"

#   retention_in_days = 14
# }

# ---------------------------------------------- #
#  Archieve file  #
# ---------------------------------------------- #
data "archive_file" "lambda_agents" {
  type = "zip"

  source_dir  = "${path.module}/api/agents"
  output_path = "${path.module}/templates/agents.zip"
}

resource "aws_s3_object" "lambda_agents" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "agents.zip"
  source = data.archive_file.lambda_agents.output_path

  etag = filemd5(data.archive_file.lambda_agents.output_path)
}


# ---------------------------------------------- #
#  TEST EVENT  Example
# ---------------------------------------------- #


locals {
  event = jsondecode(file("${path.module}/api/agents/event.json"))
}


resource "aws_lambda_invocation" "post_agents" {
  function_name = aws_lambda_function.lambda_agents.function_name
  input         = jsonencode(local.event[2])
}

resource "aws_lambda_invocation" "post_agent" {
  function_name = aws_lambda_function.lambda_agents.function_name
  input         = jsonencode(local.event[5])
}

resource "aws_lambda_invocation" "query_agents" {
  function_name = aws_lambda_function.lambda_agents.function_name
  input         = jsonencode(local.event[0])
}

resource "aws_lambda_invocation" "scan_agents" {
  function_name = aws_lambda_function.lambda_agents.function_name
  input         = jsonencode(local.event[1])
}


resource "aws_lambda_invocation" "delete_agents" {
  function_name = aws_lambda_function.lambda_agents.function_name
  input         = jsonencode(local.event[3])
}
resource "aws_lambda_invocation" "get_agent" {
  function_name = aws_lambda_function.lambda_agents.function_name
  input         = jsonencode(local.event[4])
}

resource "aws_lambda_invocation" "put_agent" {
  function_name = aws_lambda_function.lambda_agents.function_name
  input         = jsonencode(local.event[6])
}
resource "aws_lambda_invocation" "delete_agent" {
  function_name = aws_lambda_function.lambda_agents.function_name
  input         = jsonencode(local.event[7])
}
output "results" {
  value = {
    query_agents = aws_lambda_invocation.query_agents.result,
    scan_agents = aws_lambda_invocation.scan_agents.result
    post_agents = aws_lambda_invocation.post_agents.result
    delete_agents = aws_lambda_invocation.delete_agents.result
    get_agent = aws_lambda_invocation.get_agent.result
    post_agent = aws_lambda_invocation.post_agent.result
    put_agent = aws_lambda_invocation.put_agent.result
    delete_agent = aws_lambda_invocation.delete_agent.result
  }
}
