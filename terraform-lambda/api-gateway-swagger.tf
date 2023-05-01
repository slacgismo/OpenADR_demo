


# Swagger UI have to be integrated after the open API 3.0 definitons are imlemented.


resource "aws_apigatewayv2_integration" "lambda_swagger" {
  api_id = aws_apigatewayv2_api.backend.id

  integration_uri    = aws_lambda_function.lambda_swagger.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

# --------------------------------------------
#  Swagger "GET /db/swagger"
# --------------------------------------------
resource "aws_apigatewayv2_route" "get_swagger_ui" {
  api_id = aws_apigatewayv2_api.backend.id

  route_key = "GET /db/swagger"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_swagger.id}"
}


resource "aws_lambda_permission" "api_gw_swagger" {
  statement_id  = "AllowExecutionFromAPIGatewaySwagger"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_swagger.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}


