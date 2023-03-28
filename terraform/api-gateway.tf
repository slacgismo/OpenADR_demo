
#========================================
# API Gateway ROUTE
#========================================

resource "aws_apigatewayv2_integration" "lambda_battery_api" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.battery_api.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "get_battery_api" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /battery_api"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_battery_api.id}"
}

resource "aws_apigatewayv2_route" "post_battery_api" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /battery_api"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_battery_api.id}"
}

resource "aws_lambda_permission" "api_gw_battery_api" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.battery_api.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}



output "battery_api_base_url" {
  value = aws_apigatewayv2_stage.dev.invoke_url
}



#========================================
# API Gateway
#========================================

resource "aws_apigatewayv2_api" "main" {
  name         = "${var.prefix}-${var.client}-${var.environment}-devices-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "dev" {
  api_id = aws_apigatewayv2_api.main.id

  name        = "dev"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.main_api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_cloudwatch_log_group" "main_api_gw" {
  name = "/aws/api-gw/${aws_apigatewayv2_api.main.name}"

  retention_in_days = 14
}
