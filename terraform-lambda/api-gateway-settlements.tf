
resource "aws_apigatewayv2_integration" "lambda_settlements" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_settlements.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

# --------------------------------------------
#  SETTLEMENT "GET /db/settlements"
# --------------------------------------------
resource "aws_apigatewayv2_route" "query_settlements" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /db/settlements/query"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settlements.id}"
}

resource "aws_apigatewayv2_route" "scan_settlements" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /db/settlements/scan"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settlements.id}"
}
# --------------------------------------------
#  SETTLEMENT "POST /db/settlements"
# --------------------------------------------
resource "aws_apigatewayv2_route" "post_settlements" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /db/settlements"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settlements.id}"
}


# --------------------------------------------
#  SETTLEMENT "DELETE /db/settlements"
# --------------------------------------------
resource "aws_apigatewayv2_route" "delete_settlements" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "DELETE /db/settlements"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settlements.id}"
}



# --------------------------------------------
#  SETTLEMENT "GET /db/settlement/{order_id}"
# --------------------------------------------
resource "aws_apigatewayv2_route" "get_a_settlement" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /db/settlement/{order_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settlements.id}"
}

# --------------------------------------------
#  SETTLEMENT "POST /db/settlement"
# --------------------------------------------

resource "aws_apigatewayv2_route" "post_a_settlement" {
  api_id = aws_apigatewayv2_api.main.id
  # Get one agent from agent_id
  route_key = "POST /db/settlement"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settlements.id}"
}


# --------------------------------------------
#  SETTLEMENT "PUT /db/settlement/{order_id}"
# --------------------------------------------

resource "aws_apigatewayv2_route" "put_a_settlement" {
  api_id = aws_apigatewayv2_api.main.id
  # Get one agent from agent_id
  route_key = "PUT /db/settlement/{order_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settlements.id}"
}

# --------------------------------------------
#  DELETE "DELETE /db/settlement/{order_id}"
# --------------------------------------------
resource "aws_apigatewayv2_route" "delete_a_settlement" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "DELETE /db/settlement/{order_id}"
  # route_key = "POST /orders"
  target = "integrations/${aws_apigatewayv2_integration.lambda_settlements.id}"
}

resource "aws_lambda_permission" "api_gw_lambda_settlements" {
  statement_id  = "AllowExecutionFromAPIGateway-settlements"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_settlements.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

