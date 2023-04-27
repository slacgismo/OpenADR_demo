
resource "aws_apigatewayv2_integration" "lambda_settings" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_settings.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}
# --------------------------------------------
#  SETTING "GET /db/settings"
# --------------------------------------------
resource "aws_apigatewayv2_route" "query_list_of_settngs" {
  api_id = aws_apigatewayv2_api.main.id
  route_key = "GET /db/settings/query"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settings.id}"
}

resource "aws_apigatewayv2_route" "scan_list_of_settngs" {
  api_id = aws_apigatewayv2_api.main.id
  route_key = "GET /db/settings/scan"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settings.id}"
}
# --------------------------------------------
#  SETTING "POST /db/settings"
# --------------------------------------------
resource "aws_apigatewayv2_route" "post_list_of_settngs_from_device_id" {
  api_id = aws_apigatewayv2_api.main.id
  # Get a list of agents ids from resource_id
  # send payload {resource_id: "1234"}
  route_key = "POST /db/settings"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settings.id}"
}

# --------------------------------------------
#  SETTING "DELETE /db/settings"
# --------------------------------------------
resource "aws_apigatewayv2_route" "delete_list_of_settngs_from_device_id" {
  api_id = aws_apigatewayv2_api.main.id
  # Get a list of agents ids from resource_id
  # send payload {resource_id: "1234"}
  route_key = "DELETE /db/settings"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settings.id}"
}
# --------------------------------------------
#  SETTING "GET /db/setting/{setting_id}"
# --------------------------------------------
resource "aws_apigatewayv2_route" "get_a_setting" {
  api_id = aws_apigatewayv2_api.main.id
  route_key = "GET /db/setting/{setting_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settings.id}"
}

# --------------------------------------------
#  SETTING "POST /db/setting"
# --------------------------------------------
resource "aws_apigatewayv2_route" "post_a_setting" {
  api_id = aws_apigatewayv2_api.main.id
  route_key = "POST /db/setting"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settings.id}"
}

# --------------------------------------------
#  SETTING "PUT /db/setting/{setting_id}"
# --------------------------------------------
resource "aws_apigatewayv2_route" "put_setting_from_device_id" {
  api_id = aws_apigatewayv2_api.main.id
  route_key = "PUT /db/setting/{setting_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_settings.id}"
}
# --------------------------------------------
#  SETTING "DELETE /db/setting/{setting_id}"
# --------------------------------------------

resource "aws_apigatewayv2_route" "delete_a_setting" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "DELETE /db/setting/{setting_id}"
  target = "integrations/${aws_apigatewayv2_integration.lambda_settings.id}"
}

resource "aws_lambda_permission" "api_gw_lambda_settings" {
  statement_id  = "AllowExecutionFromAPIGateway-settings"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_settings.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

