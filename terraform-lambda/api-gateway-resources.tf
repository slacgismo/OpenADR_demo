
resource "aws_apigatewayv2_integration" "lambda_resources" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.lambda_resources.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

# resource "aws_apigatewayv2_route" "get_a_list_of_resources" {
#   api_id = aws_apigatewayv2_api.main.id
#   #GET /db/resources?<args...>, Get a list of resource ids
  
#   route_key = "GET /db/resources"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_resources.id}"
# }


resource "aws_apigatewayv2_route" "get_a_resource" {
  api_id = aws_apigatewayv2_api.main.id
  #GET /db/resource/<resource_id> -- Gets data about a system resource.
  
  route_key = "GET /db/resource/{resource_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_resources.id}"
}



resource "aws_apigatewayv2_route" "put_a_resource" {
 # PUT /db/resource/<resource_id>
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "PUT /db/resource/{resource_id}"
  target = "integrations/${aws_apigatewayv2_integration.lambda_resources.id}"
}

resource "aws_apigatewayv2_route" "delete_a_resource" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "DELETE /db/resource/{resource_id}"
  target = "integrations/${aws_apigatewayv2_integration.lambda_resources.id}"
}

resource "aws_lambda_permission" "api_gw_lambda_resources" {
  statement_id  = "AllowExecutionFromAPIGateway-resources"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_agents.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

