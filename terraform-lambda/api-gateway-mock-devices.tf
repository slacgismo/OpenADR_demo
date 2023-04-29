
# resource "aws_apigatewayv2_integration" "lambda_mock_devices" {
#   api_id = aws_apigatewayv2_api.backend.id

#   integration_uri    = aws_lambda_function.lambda_mock_devices.invoke_arn
#   integration_type   = "AWS_PROXY"
#   integration_method = "POST"
# }
# --------------------------------------------
#  MOCK_DEVICE "GET /db/mock_device"
# --------------------------------------------
# resource "aws_apigatewayv2_route" "get_mock_device_data" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "GET /db/mock_device"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_mock_devices.id}"
# }

# # --------------------------------------------
# #  MOCK_DEVICE "PUT /db/mock_device"
# # --------------------------------------------
# resource "aws_apigatewayv2_route" "put_mock_device_data" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "PUT /db/mock_device"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_mock_devices.id}"
# }


# resource "aws_lambda_permission" "api_gw_lambda_mock_devices" {
#   statement_id  = "AllowExecutionFromAPIGateway-mock-devices"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.lambda_mock_devices.function_name
#   principal     = "apigateway.amazonaws.com"

#   source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
# }

