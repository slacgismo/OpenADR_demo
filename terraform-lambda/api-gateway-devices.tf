

# --------------------------------------------
#  LAMNDA DEVICES
# --------------------------------------------

resource "aws_apigatewayv2_integration" "lamdba_devices" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lamdba_devices.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}


# --------------------------------------------
#  DEVICES "GET /db/devices/{agent_id}"
# --------------------------------------------

resource "aws_apigatewayv2_route" "get_list_of_devices_from_agent_id" {
  api_id = aws_apigatewayv2_api.main.id
  route_key = "GET /db/devices/{agent_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lamdba_devices.id}"
}
# --------------------------------------------
#  DEVICES "POST /db/devices"
# --------------------------------------------

resource "aws_apigatewayv2_route" "post_list_of_devices_from_agent_id" {
  api_id = aws_apigatewayv2_api.main.id
  route_key = "POST /db/devices"
  target    = "integrations/${aws_apigatewayv2_integration.lamdba_devices.id}"
}

# --------------------------------------------
#  DEVICES "PUT /db/devices"
# --------------------------------------------



# --------------------------------------------
#  DEVICES "DELETE /db/devices"
# --------------------------------------------

resource "aws_apigatewayv2_route" "delete_list_of_devices_from_agent_id" {
  api_id = aws_apigatewayv2_api.main.id
  route_key = "DELETE /db/devices"
  target    = "integrations/${aws_apigatewayv2_integration.lamdba_devices.id}"
}

# --------------------------------------------
#  DEVICE "GET /db/device/{device_id}"
# --------------------------------------------

resource "aws_apigatewayv2_route" "get_a_device" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /db/device/{device_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lamdba_devices.id}"
}

# --------------------------------------------
#  DEVICE "POST /db/device/{device_id}"
# --------------------------------------------

resource "aws_apigatewayv2_route" "post_a_device" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /db/device"
  target    = "integrations/${aws_apigatewayv2_integration.lamdba_devices.id}"
}

# --------------------------------------------
#  DEVICE "PUT /db/device/{device_id}"
# --------------------------------------------

resource "aws_apigatewayv2_route" "put_a_device" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "PUT /db/device/{device_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lamdba_devices.id}"
}

# --------------------------------------------
#  DEVICE "DELETE /db/device/{device_id}"
# --------------------------------------------


resource "aws_apigatewayv2_route" "delete_a_device" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "DELETE /db/device/{device_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lamdba_devices.id}"
}

resource "aws_lambda_permission" "api_gw_device" {
  statement_id  = "AllowExecutionFromAPIGateway-devicces"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lamdba_devices.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

