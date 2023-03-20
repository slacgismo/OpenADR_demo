
resource "aws_apigatewayv2_integration" "lambda_participated_vens" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.participated_vens.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "get_participated_vens" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /participated_vens"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_participated_vens.id}"
}

resource "aws_apigatewayv2_route" "post_participated_vens" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /participated_vens"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_participated_vens.id}"
}

resource "aws_lambda_permission" "api_gw_participated_vens" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.participated_vens.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

output "participated_vens_base_url" {
  value = aws_apigatewayv2_stage.dev.invoke_url
}