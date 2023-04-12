
resource "aws_apigatewayv2_integration" "lambda_devices" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_devices.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "get_lambda_devices" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /device/{device_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_devices.id}"
}

resource "aws_apigatewayv2_route" "put_lambda_devices" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "PUT /device/{device_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_devices.id}"
}



resource "aws_apigatewayv2_route" "delete_lambda_devices" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "DELETE /device/{device_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_devices.id}"
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_devices.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

output "devices_devices_base_url" {
  value = "${aws_apigatewayv2_stage.dev.invoke_url}/${aws_apigatewayv2_route.put_lambda_devices.route_key}"

}