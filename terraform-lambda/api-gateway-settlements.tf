
resource "aws_apigatewayv2_integration" "lambda_settlements" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_settlements.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

# resource "aws_apigatewayv2_route" "get_list_of_settlements_from_order_id" {
#   api_id = aws_apigatewayv2_api.main.id

#   route_key = "GET /db/settlements/{order_id}"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_settlements.id}"
# }

resource "aws_apigatewayv2_route" "put_settlement_from_order_id" {
  api_id = aws_apigatewayv2_api.main.id
  # Get one agent from agent_id
  route_key = "PUT /db/settlement/{order_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settlements.id}"
}


resource "aws_apigatewayv2_route" "delete_lambda_settlements" {
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

