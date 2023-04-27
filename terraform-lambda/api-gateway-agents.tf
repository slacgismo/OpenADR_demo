

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
# AGENTS "GET /db/agents/query"
# get_items_action = "query" 
# query: query items from hash_key or hash_key + range_key with global secondary index (gsi)
# if query :
# queryStringParameters: {
#   gsi_name: string,
#   key_value: string,
#   key_name: string,
#   key_type: string, // optional 'S' | 'N' dedault = 'S'
#   range_key: string,  // optional default = None
#   range_key_value: string, // optional 'S' | 'N' dedault = 'N'
#   start_from: string, // optional timstamp
#   end_at: string, // optional timstamp
#}

# --------------------------------------------

# resource "aws_apigatewayv2_route" "query_agents" {
#   api_id = aws_apigatewayv2_api.main.id
#   route_key = "GET /db/agents/query"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
# }

# --------------------------------------------
# AGENTS "GET /db/agents/scan"
# scan: scan all items with key that not is hash_key nor one of global secondary index key
# if scan:
# queryStringParameters: {
#  key_name: string,
#  key_value: string,
#  key_type: string, //optional 'S' | 'N' dedault = 'S'
#}
# --------------------------------------------
# resource "aws_apigatewayv2_route" "scan_agents" {
#   api_id = aws_apigatewayv2_api.main.id
#   route_key = "GET /db/agents/scan"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
# }



# --------------------------------------------
# AGENTS "POST /db/agents"
# --------------------------------------------
# resource "aws_apigatewayv2_route" "post_list_agents" {
#   api_id = aws_apigatewayv2_api.main.id
#   route_key = "POST /db/agents"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
# }
# --------------------------------------------
# AGENTS "PUT /db/agents"
# No need to update all agents
# --------------------------------------------

# --------------------------------------------
# AGENTS "GET /db/agents"
# --------------------------------------------

# resource "aws_apigatewayv2_route" "delete_list_agents" {
#   api_id = aws_apigatewayv2_api.main.id
#   route_key = "DELETE /db/agents"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
# }


# --------------------------------------------
# AGENT
# --------------------------------------------

# --------------------------------------------
# AGENT "GET /db/agent/{agent_id}"
# --------------------------------------------
# resource "aws_apigatewayv2_route" "get_one_agent" {
#   api_id = aws_apigatewayv2_api.main.id
#   # Get one agent from agent_id
#   route_key = "GET /db/agent/{agent_id}"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
# }

# --------------------------------------------
# create agent
# AGENT "POST /db/agent"  
# --------------------------------------------
# resource "aws_apigatewayv2_route" "post_single_agent" {
#   api_id    = aws_apigatewayv2_api.main.id
#   route_key = "POST /db/agent"
#   target = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
# }


# --------------------------------------------
# update agent
# AGENT "PUT /db/agent/{agent_id}" 
# --------------------------------------------
# resource "aws_apigatewayv2_route" "put_single_agent" {
#   api_id    = aws_apigatewayv2_api.main.id
#   route_key = "PUT /db/agent/{agent_id}"
#   target = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
# }
# --------------------------------------------
# AGENT "DELETE /db/agent/{agent_id}" 
# --------------------------------------------

# resource "aws_apigatewayv2_route" "delete_single_agent" {
#   api_id    = aws_apigatewayv2_api.main.id
#   route_key = "DELETE /db/agent/{agent_id}"
#   target = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
# }

resource "aws_lambda_permission" "api_gw_agent" {
  statement_id  = "AllowExecutionFromAPIGatewa-agent"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_agents.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

