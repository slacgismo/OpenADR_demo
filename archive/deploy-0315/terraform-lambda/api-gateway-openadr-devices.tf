
resource "aws_apigatewayv2_integration" "lambda_openadr_devices" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.openadr_devices.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "get_openadr_devices" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /openadr_devices"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_openadr_devices.id}"
}

resource "aws_apigatewayv2_route" "post_openadr_devices" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /openadr_devices"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_openadr_devices.id}"
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.openadr_devices.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

output "openadr_devices_base_url" {
  value = aws_apigatewayv2_stage.dev.invoke_url
}