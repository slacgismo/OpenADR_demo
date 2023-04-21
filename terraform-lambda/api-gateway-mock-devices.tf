
resource "aws_apigatewayv2_integration" "lambda_mock_devices" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_mock_devices.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "get_mock_device_data" {
  api_id = aws_apigatewayv2_api.main.id
  # Get a list of agents ids from resource_id
  # send payload {resource_id: "1234"}
  route_key = "GET /db/mock_device/{device_brand}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_mock_devices.id}"
}



resource "aws_lambda_permission" "api_gw_lambda_mock_devices" {
  statement_id  = "AllowExecutionFromAPIGateway-mock-devices"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_mock_devices.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

