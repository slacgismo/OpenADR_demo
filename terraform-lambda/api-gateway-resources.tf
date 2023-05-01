
# resource "aws_apigatewayv2_integration" "lambda_resources" {
#   api_id = aws_apigatewayv2_api.backend.id

#   integration_uri    = aws_lambda_function.lambda_resources.invoke_arn
#   integration_type   = "AWS_PROXY"
#   integration_method = "POST"
# }

# --------------------------------------------
#  RESOURCES "GET /db/resources"
# --------------------------------------------

# resource "aws_apigatewayv2_route" "query_resources" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "GET /db/resources/query"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_resources.id}"
# }

# resource "aws_apigatewayv2_route" "scan_resources" {
#   api_id = aws_apigatewayv2_api.backend.id

#   route_key = "GET /db/resources/scan"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_orders.id}"
# }

# # --------------------------------------------
# #  RESOURCES "POST /db/resources"
# # --------------------------------------------

# resource "aws_apigatewayv2_route" "post_resources" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "POST /db/resources"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_resources.id}"
# }


# # --------------------------------------------
# #  RESOURCES "DELETE /db/resources"
# # --------------------------------------------

# resource "aws_apigatewayv2_route" "delete_resources" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "DELETE /db/resources"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_resources.id}"
# }

# # --------------------------------------------
# #  RESOURCE "GET /db/resource/{resource_id}"
# # --------------------------------------------
# resource "aws_apigatewayv2_route" "get_a_resource" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "GET /db/resource/{resource_id}"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_resources.id}"
# }

# # --------------------------------------------
# #  RESOURCE "POST /db/resource/{resource_id}"
# # --------------------------------------------

# resource "aws_apigatewayv2_route" "post_a_resource" {
#   api_id    = aws_apigatewayv2_api.backend.id
#   route_key = "POST /db/resource"
#   target = "integrations/${aws_apigatewayv2_integration.lambda_resources.id}"
# }


# # --------------------------------------------
# #  RESOURCE "PUT /db/resource/{resource_id}"
# # --------------------------------------------

# resource "aws_apigatewayv2_route" "put_a_resource" {
#   api_id    = aws_apigatewayv2_api.backend.id
#   route_key = "PUT /db/resource/{resource_id}"
#   target = "integrations/${aws_apigatewayv2_integration.lambda_resources.id}"
# }

# # --------------------------------------------
# #  RESOURCE "DELETE /db/resource/{resource_id}"
# # --------------------------------------------

# resource "aws_apigatewayv2_route" "delete_a_resource" {
#   api_id    = aws_apigatewayv2_api.backend.id
#   route_key = "DELETE /db/resource/{resource_id}"
#   target = "integrations/${aws_apigatewayv2_integration.lambda_resources.id}"
# }

resource "aws_lambda_permission" "api_gw_lambda_resources" {
  statement_id  = "AllowExecutionFromAPIGateway-resources"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_resources.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}

