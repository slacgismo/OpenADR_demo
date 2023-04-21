
resource "aws_apigatewayv2_integration" "lambda_meters" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_meters.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

# resource "aws_apigatewayv2_route" "get_list_of_meters" {
#   api_id = aws_apigatewayv2_api.main.id

#   #Get /db/meters, Get a list of meter readings.

#   route_key = "GET /db/meters"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_meters.id}"
# }

resource "aws_apigatewayv2_route" "get_a_meter_from_device_id" {
  api_id = aws_apigatewayv2_api.main.id

  #Get /db/meter/{device_id}, Get a meter from device id.

  route_key = "GET /db/meter/{device_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_meters.id}"
}


resource "aws_apigatewayv2_route" "put_a_meter" {
  api_id = aws_apigatewayv2_api.main.id

  #PUT /db/meter/<meter_id>

  route_key = "PUT /db/meter/{metere_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_meters.id}"
}

resource "aws_apigatewayv2_route" "delete_a_meter" {
  api_id = aws_apigatewayv2_api.main.id

  #Delete /db/meter/<meter_id>

  route_key = "DELETE /db/meter/{meter_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_meters.id}"
}

resource "aws_lambda_permission" "api_gw_meters" {
  statement_id  = "AllowExecutionFromAPIGateway-meters"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_meters.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

