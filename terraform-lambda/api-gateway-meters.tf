
# resource "aws_apigatewayv2_integration" "lambda_meters" {
#   api_id = aws_apigatewayv2_api.backend.id

#   integration_uri    = aws_lambda_function.lambda_meters.invoke_arn
#   integration_type   = "AWS_PROXY"
#   integration_method = "POST"
# }


# --------------------------------------------
#  METER "GET /db/meters"
# --------------------------------------------
# resource "aws_apigatewayv2_route" "query_meters" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "GET /db/meters/query"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_meters.id}"
# }
# resource "aws_apigatewayv2_route" "scan_meters" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "GET /db/meters/scan"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_meters.id}"
# }


# # --------------------------------------------
# #  METER "DELETE /db/meters"
# # --------------------------------------------
# resource "aws_apigatewayv2_route" "delete_meters" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "DELETE /db/meters"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_meters.id}"
# }



# # --------------------------------------------
# #  METER "GET /db/meter/{meter_id}"
# # --------------------------------------------

# resource "aws_apigatewayv2_route" "get_a_meter_from_device_id" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "GET /db/meter/{meter_id}"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_meters.id}"
# }
# # --------------------------------------------
# #  METER "POST /db/meter"
# # --------------------------------------------

# resource "aws_apigatewayv2_route" "post_a_meter" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "POST /db/meter"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_meters.id}"
# }

# # --------------------------------------------
# #  METER "PUT /db/meter/{meter_id}"
# # --------------------------------------------

# resource "aws_apigatewayv2_route" "put_a_meter" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "PUT /db/meter/{metere_id}"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_meters.id}"
# }

# # --------------------------------------------
# #  METER "DELETE /db/meter/{meter_id}"
# # --------------------------------------------

# resource "aws_apigatewayv2_route" "delete_a_meter" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "DELETE /db/meter/{meter_id}"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_meters.id}"
# }

resource "aws_lambda_permission" "api_gw_meters" {
  statement_id  = "AllowExecutionFromAPIGateway-meters"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_meters.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}

