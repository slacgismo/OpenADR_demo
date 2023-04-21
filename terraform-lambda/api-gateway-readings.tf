
resource "aws_apigatewayv2_integration" "lambda_readings" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_readings.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

# resource "aws_apigatewayv2_route" "get_lists_of_readings_from_meter_id" {
#   # GET /db/reading/{reading_id}
#   api_id = aws_apigatewayv2_api.main.id

#   route_key = "GET /db/readings/{meter_id}"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_readings.id}"
# }

resource "aws_apigatewayv2_route" "put_a_reading_from_meter_id" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "PUT /db/reading/{meter_id}"
  # route_key = "POST /orders"
  target = "integrations/${aws_apigatewayv2_integration.lambda_readings.id}"
}

resource "aws_apigatewayv2_route" "delete_a_reading" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "DELETE /db/reading/{reading_id}"
  # route_key = "POST /orders"
  target = "integrations/${aws_apigatewayv2_integration.lambda_readings.id}"
}


resource "aws_lambda_permission" "api_lambda_readings" {
  statement_id  = "AllowExecutionFromAPIGateway-readings"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_readings.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

