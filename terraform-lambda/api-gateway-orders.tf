
resource "aws_apigatewayv2_integration" "lambda_orders" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_orders.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "get_lambda_orders" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /db/order"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_orders.id}"
}

resource "aws_apigatewayv2_route" "post_lambda_orders" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "PUT /db/order/{device_id}"
  # route_key = "POST /orders"
  target = "integrations/${aws_apigatewayv2_integration.lambda_orders.id}"
}

resource "aws_lambda_permission" "api_gw_lambda_orders" {
  statement_id  = "AllowExecutionFromAPIGateway-orders"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_orders.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

# output "orders_api_url" {
#   value = "${aws_apigatewayv2_stage.dev.invoke_url}/${aws_apigatewayv2_route.get_lambda_orders.route_key}"
# }