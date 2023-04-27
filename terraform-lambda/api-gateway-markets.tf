
resource "aws_apigatewayv2_integration" "lambda_markets" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_markets.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

# --------------------------------------------
#  MARKET "GET /db/markets"
# --------------------------------------------
resource "aws_apigatewayv2_route" "query_markets" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /db/markets/query"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_markets.id}"
}
resource "aws_apigatewayv2_route" "scan_markets" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /db/markets/scan"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_markets.id}"
}
# --------------------------------------------
#  MARKETS "POST /db/markets"
# --------------------------------------------
resource "aws_apigatewayv2_route" "post_markets" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /db/markets"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_markets.id}"
}

# --------------------------------------------
#  MARKETS "DELETE /db/markets"
# --------------------------------------------
resource "aws_apigatewayv2_route" "delete_markets" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "DELETE /db/markets"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_markets.id}"
}


# --------------------------------------------
#  MARKETS "GET /db/market/{market_id}"
# --------------------------------------------

resource "aws_apigatewayv2_route" "get_one_market" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /db/market/{market_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_markets.id}"
}
# --------------------------------------------
#  MARKET "POST /db/market"
# --------------------------------------------
resource "aws_apigatewayv2_route" "post_market" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "POST /db/market"
  # route_key = "POST /orders"
  target = "integrations/${aws_apigatewayv2_integration.lambda_markets.id}"
}
# --------------------------------------------
#  MARKET "PUT /db/market/{market_id}"
# --------------------------------------------
resource "aws_apigatewayv2_route" "put_market" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "PUT /db/market/{market_id}"
  # route_key = "POST /orders"
  target = "integrations/${aws_apigatewayv2_integration.lambda_markets.id}"
}
# --------------------------------------------
#  MARKET "DELETE /db/market/{market_id}"
# --------------------------------------------
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

