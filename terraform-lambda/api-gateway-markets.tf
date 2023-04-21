
resource "aws_apigatewayv2_integration" "lambda_markets" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_markets.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

# resource "aws_apigatewayv2_route" "get_lambda_markets" {
#   api_id = aws_apigatewayv2_api.main.id

#   route_key = "GET /db/all-markets-status"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_markets.id}"
# }

# resource "aws_apigatewayv2_route" "get_lambda_agents_from_resources" {
#   api_id = aws_apigatewayv2_api.main.id

#   route_key = "GET /db/markets"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_markets.id}"
# }


resource "aws_apigatewayv2_route" "get_one_market" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /db/market/{market_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_markets.id}"
}

resource "aws_apigatewayv2_route" "put_market" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "PUT /db/market/{market_id}"
  # route_key = "POST /orders"
  target = "integrations/${aws_apigatewayv2_integration.lambda_markets.id}"
}

resource "aws_apigatewayv2_route" "delete_lambda_markets" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "DELETE /db/market/{market_id}"
  # route_key = "POST /orders"
  target = "integrations/${aws_apigatewayv2_integration.lambda_markets.id}"
}

resource "aws_lambda_permission" "api_gw_lambda_markets" {
  statement_id  = "AllowExecutionFromAPIGateway-markets"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_markets.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

