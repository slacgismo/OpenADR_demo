
resource "aws_apigatewayv2_integration" "lambda_weather" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_weather.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}


# --------------------------------------------
#  WEATHERS "GET /db/weathers"
# --------------------------------------------
resource "aws_apigatewayv2_route" "get_a_list_of_weather" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /db/weathers"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_weather.id}"
}
# --------------------------------------------
#  WEATHERS "POST /db/weathers"
# --------------------------------------------
resource "aws_apigatewayv2_route" "post_a_list_of_weather" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /db/weathers"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_weather.id}"
}



# --------------------------------------------
#  WEATHERS "DELETE /db/weathers"
# --------------------------------------------
resource "aws_apigatewayv2_route" "delete_weathers" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "DELETE /db/weathers"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_weather.id}"
}



# --------------------------------------------
#  WEATHER "GET /db/weather"
#  query weather from location (zip code)
#  payload start_from (timestamp), end_at(timsstamp)
# --------------------------------------------
resource "aws_apigatewayv2_route" "get_a_weather" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /db/weather"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_weather.id}"
}
# --------------------------------------------
#  WEATHER "POST /db/weather"
# --------------------------------------------
resource "aws_apigatewayv2_route" "post_a_weather" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /db/weather"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_weather.id}"
}

# --------------------------------------------
#  WEATHER "PUT /db/weather/{zipcode}"
# --------------------------------------------
resource "aws_apigatewayv2_route" "put_a_weather" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "PUT /db/weather/{weather_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_weather.id}"
}

# --------------------------------------------
#  WEATHER "DELETE /db/weather/{weather_id}"
# --------------------------------------------
resource "aws_apigatewayv2_route" "delete_a_weather" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "DELETE /db/weather/{weather_id}"
  target = "integrations/${aws_apigatewayv2_integration.lambda_weather.id}"
}

resource "aws_lambda_permission" "api_gw_lambda_weather" {
  statement_id  = "AllowExecutionFromAPIGateway-weather"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_weather.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

