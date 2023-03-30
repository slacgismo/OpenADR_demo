
resource "aws_apigatewayv2_integration" "lambda_meters" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_meters.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "get_lambda_meters" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /db/meter"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_meters.id}"
}

resource "aws_apigatewayv2_route" "post_lambda_meters" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "PUT /db/meter/{device_id}/{meter_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_meters.id}"
}

resource "aws_lambda_permission" "api_gw_meters" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_meters.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

output "meters_api_base_url" {
  value = "${aws_apigatewayv2_stage.dev.invoke_url}/${aws_apigatewayv2_route.get_lambda_meters.route_key}"
}
