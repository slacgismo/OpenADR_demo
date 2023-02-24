
resource "aws_apigatewayv2_integration" "lambda_market_prices" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.market_prices.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "get_market_prices" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /market_prices"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_market_prices.id}"
}

resource "aws_apigatewayv2_route" "post_market_prices" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /market_prices"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_market_prices.id}"
}

resource "aws_lambda_permission" "api_gw_market_prices" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.market_prices.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

output "market_prices_base_url" {
  value = aws_apigatewayv2_stage.dev.invoke_url
}