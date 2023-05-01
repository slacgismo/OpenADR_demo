
# resource "aws_apigatewayv2_integration" "lambda_readings" {
#   api_id = aws_apigatewayv2_api.backend.id

#   integration_uri    = aws_lambda_function.lambda_readings.invoke_arn
#   integration_type   = "AWS_PROXY"
#   integration_method = "POST"
# }
# --------------------------------------------
#  READINGS "GET /db/readings"
# --------------------------------------------
# resource "aws_apigatewayv2_route" "query_readings" {
#   # GET /db/reading/{reading_id}
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "GET /db/readings/query"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_readings.id}"
# }

# resource "aws_apigatewayv2_route" "scan_readings" {
#   api_id = aws_apigatewayv2_api.backend.id

#   route_key = "GET /db/readings/scan"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_orders.id}"
# }

# # --------------------------------------------
# #  READINGS "POST /db/readings"
# # --------------------------------------------
# resource "aws_apigatewayv2_route" "post_readings" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "POST /db/readings"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_readings.id}"
# }

# # --------------------------------------------
# #  READINGS "DELETE /db/readings"
# # --------------------------------------------
# resource "aws_apigatewayv2_route" "delete_readings" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "DELETE /db/readings"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_readings.id}"
# }

# # --------------------------------------------
# #  READING "POST /db/reading"
# # --------------------------------------------
# resource "aws_apigatewayv2_route" "post_a_reading_from_meter_id" {
#   api_id    = aws_apigatewayv2_api.backend.id
#   route_key = "POST /db/reading"
#   # route_key = "POST /orders"
#   target = "integrations/${aws_apigatewayv2_integration.lambda_readings.id}"
# }

# # --------------------------------------------
# #  READING "PUT /db/reading/{meter_id}"
# # --------------------------------------------
# resource "aws_apigatewayv2_route" "put_a_reading_from_meter_id" {
#   api_id    = aws_apigatewayv2_api.backend.id
#   route_key = "PUT /db/reading/{meter_id}"
#   # route_key = "POST /orders"
#   target = "integrations/${aws_apigatewayv2_integration.lambda_readings.id}"
# }
# # --------------------------------------------
# #  READING "DELETE /db/reading/{meter_id}"
# # --------------------------------------------
# resource "aws_apigatewayv2_route" "delete_a_reading" {
#   api_id    = aws_apigatewayv2_api.backend.id
#   route_key = "DELETE /db/reading/{reading_id}"
#   # route_key = "POST /orders"
#   target = "integrations/${aws_apigatewayv2_integration.lambda_readings.id}"
# }


resource "aws_lambda_permission" "api_lambda_readings" {
  statement_id  = "AllowExecutionFromAPIGateway-readings"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_readings.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}

