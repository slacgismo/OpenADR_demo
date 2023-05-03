
# --------------------------------------------
# 1 AGENTS
# --------------------------------------------

resource "aws_lambda_permission" "api_gw_agent" {
  statement_id  = "AllowExecutionFromAPIGatewa-agent"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_agents.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}

# --------------------------------------------
# 2 AUCTIONS
# --------------------------------------------


resource "aws_lambda_permission" "api_gw_lambda_auctions" {
  statement_id  = "AllowExecutionFromAPIGateway-auctions"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_auctions.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}

# --------------------------------------------
# 3 DEVICES
# --------------------------------------------

resource "aws_lambda_permission" "api_gw_device" {
  statement_id  = "AllowExecutionFromAPIGateway-devicces"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_devices.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}

# --------------------------------------------
# 4 DISPATCHES
# --------------------------------------------

resource "aws_lambda_permission" "api_gw_dispatches" {
  statement_id  = "AllowExecutionFromAPIGateway-dispatches"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.dispatches.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}
# --------------------------------------------
# 5 MARKETS
# --------------------------------------------

resource "aws_lambda_permission" "api_gw_lambda_markets" {
  statement_id  = "AllowExecutionFromAPIGateway-markets"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_markets.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}

# --------------------------------------------
# 6 METERS
# --------------------------------------------

resource "aws_lambda_permission" "api_gw_meters" {
  statement_id  = "AllowExecutionFromAPIGateway-meters"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_meters.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}


# --------------------------------------------
# 7 MOCK DEVICES
# --------------------------------------------

resource "aws_lambda_permission" "api_gw_lambda_mock_devices" {
  statement_id  = "AllowExecutionFromAPIGateway-mock-devices"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_mock_devices.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}

# --------------------------------------------
# 8 ORDERS
# --------------------------------------------

resource "aws_lambda_permission" "api_gw_lambda_orders" {
  statement_id  = "AllowExecutionFromAPIGateway-orders"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_orders.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}
# --------------------------------------------
# 9 READINGS
# --------------------------------------------

resource "aws_lambda_permission" "api_lambda_readings" {
  statement_id  = "AllowExecutionFromAPIGateway-readings"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_readings.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}

# --------------------------------------------
# 10 RESOURCES
# --------------------------------------------

resource "aws_lambda_permission" "api_gw_lambda_resources" {
  statement_id  = "AllowExecutionFromAPIGateway-resources"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_resources.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}

# --------------------------------------------
# 11 SETTINGS
# --------------------------------------------

resource "aws_lambda_permission" "api_gw_lambda_settings" {
  statement_id  = "AllowExecutionFromAPIGateway-settings"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_settings.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}


# --------------------------------------------
# 12 SETTLEMENTS
# --------------------------------------------

resource "aws_lambda_permission" "api_gw_lambda_settlements" {
  statement_id  = "AllowExecutionFromAPIGateway-settlements"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_settlements.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}

# --------------------------------------------
# 13 WEATHERS
# --------------------------------------------

resource "aws_lambda_permission" "api_gw_lambda_weather" {
  statement_id  = "AllowExecutionFromAPIGateway-weather"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_weather.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}


