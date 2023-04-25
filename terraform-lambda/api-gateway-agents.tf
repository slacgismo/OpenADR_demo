

resource "aws_apigatewayv2_integration" "lambda_agents" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_agents.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}


# --------------------------------------------
#  AGENTS
# --------------------------------------------


# --------------------------------------------
# AGENTS "GET /db/agents"
# --------------------------------------------
resource "aws_apigatewayv2_route" "get_list_agents_from_resource_id" {
  api_id = aws_apigatewayv2_api.main.id
  route_key = "GET /db/agents/{resource_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
}
# --------------------------------------------
# AGENTS "POST /db/agents"
# --------------------------------------------
resource "aws_apigatewayv2_route" "post_list_agents" {
  api_id = aws_apigatewayv2_api.main.id
  route_key = "POST /db/agents"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
}
# --------------------------------------------
# AGENTS "PUT /db/agents"
# --------------------------------------------
resource "aws_apigatewayv2_route" "put_list_agents" {
  api_id = aws_apigatewayv2_api.main.id
  route_key = "PUT /db/agents"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
}
# --------------------------------------------
# AGENTS "GET /db/agents"
# --------------------------------------------

resource "aws_apigatewayv2_route" "delete_list_agents" {
  api_id = aws_apigatewayv2_api.main.id
  route_key = "DELETE /db/agents"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
}


# --------------------------------------------
# AGENT
# --------------------------------------------

# --------------------------------------------
# AGENT "GET /db/agent/{agent_id}"
# --------------------------------------------
resource "aws_apigatewayv2_route" "get_one_agent" {
  api_id = aws_apigatewayv2_api.main.id
  # Get one agent from agent_id
  route_key = "GET /db/agent/{agent_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
}

# --------------------------------------------
# create agent
# AGENT "POST /db/agent"  
# --------------------------------------------
resource "aws_apigatewayv2_route" "post_single_agent" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "POST /db/agent"
  target = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
}


# --------------------------------------------
# update agent
# AGENT "PUT /db/agent/{agent_id}" 
# --------------------------------------------
resource "aws_apigatewayv2_route" "put_single_agent" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "PUT /db/agent/{agent_id}"
  target = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
}
# --------------------------------------------
# AGENT "DELETE /db/agent/{agent_id}" 
# --------------------------------------------

resource "aws_apigatewayv2_route" "delete_single_agent" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "DELETE /db/agent/{agent_id}"
  target = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
}

resource "aws_lambda_permission" "api_gw_agent" {
  statement_id  = "AllowExecutionFromAPIGatewa-agent"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_agents.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

