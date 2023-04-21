
resource "aws_apigatewayv2_integration" "lambda_weather" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_weather.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "get_weather_from_location" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /db/weather/{location}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_weather.id}"
}

resource "aws_apigatewayv2_route" "put_weather_from_location" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "PUT /db/weather/{location}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_weather.id}"
}


resource "aws_apigatewayv2_route" "delete_lambda_weather" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "DELETE /db/weather/{location}"
  target = "integrations/${aws_apigatewayv2_integration.lambda_weather.id}"
}

resource "aws_lambda_permission" "api_gw_lambda_weather" {
  statement_id  = "AllowExecutionFromAPIGateway-weather"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_weather.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

