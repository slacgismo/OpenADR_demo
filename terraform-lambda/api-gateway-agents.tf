
resource "aws_apigatewayv2_integration" "lambda_agents" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_agents.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

# resource "aws_apigatewayv2_route" "get_list_agents_from_resource_id" {
#   api_id = aws_apigatewayv2_api.main.id
#   # Get a list of agents ids from resource_id
#   # send payload {resource_id: "1234"}
#   route_key = "GET /db/agents/{resource_id}"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
# }




resource "aws_apigatewayv2_route" "get_one_agents" {
  api_id = aws_apigatewayv2_api.main.id
  # Get one agent from agent_id
  route_key = "GET /db/agent/{agent_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
}

resource "aws_apigatewayv2_route" "put_lambda_agents" {
 # Put an agent record to table
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "PUT /db/agent/{agent_id}"
  # route_key = "POST /orders"
  target = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
}

resource "aws_apigatewayv2_route" "delete_lambda_agents" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "DELETE /db/agent/{agent_id}"
  # route_key = "POST /orders"
  target = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
}

resource "aws_lambda_permission" "api_gw_agents" {
  statement_id  = "AllowExecutionFromAPIGatewa-agents"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_agents.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

