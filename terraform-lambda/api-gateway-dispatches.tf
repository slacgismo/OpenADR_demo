
resource "aws_apigatewayv2_integration" "lambda_dispatches" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.dispatches.invoke_arn
  integration_type   = "AWS_PROXY"
   integration_method = "POST"
}

resource "aws_apigatewayv2_route" "get_dispatches" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "GET /db/dispatch/{order_id}"
  # route_key = "GET /dispatches"
  target = "integrations/${aws_apigatewayv2_integration.lambda_dispatches.id}"
}

resource "aws_apigatewayv2_route" "post_dispatches" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "PUT /db/dispatch"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_dispatches.id}"
}

resource "aws_lambda_permission" "api_gw_dispatches" {
  statement_id  = "AllowExecutionFromAPIGateway-dispatches"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.dispatches.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

# output "dispatches_vens_base_url" {
#   value = "${aws_apigatewayv2_stage.dev.invoke_url}/${aws_apigatewayv2_route.get_dispatches.route_key}"
# }