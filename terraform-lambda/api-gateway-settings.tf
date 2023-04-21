
resource "aws_apigatewayv2_integration" "lambda_settings" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_settings.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

# resource "aws_apigatewayv2_route" "get_list_of_settngs_from_device_id" {
#   api_id = aws_apigatewayv2_api.main.id
#   # Get a list of agents ids from resource_id
#   # send payload {resource_id: "1234"}
#   route_key = "GET /db/settings/{device_id}"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_settings.id}"
# }

resource "aws_apigatewayv2_route" "put_setting_from_device_id" {
  api_id = aws_apigatewayv2_api.main.id
  # Get one agent from agent_id
  route_key = "PUT /db/setting/{device_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settings.id}"
}


resource "aws_apigatewayv2_route" "delete_lambda_settings" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "DELETE /db/setting/{setting_id}"
  # route_key = "POST /orders"
  target = "integrations/${aws_apigatewayv2_integration.lambda_settings.id}"
}

resource "aws_lambda_permission" "api_gw_lambda_settings" {
  statement_id  = "AllowExecutionFromAPIGateway-settings"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_settings.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

