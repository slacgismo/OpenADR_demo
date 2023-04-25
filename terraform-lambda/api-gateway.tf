resource "aws_apigatewayv2_api" "main" {
  name          ="${var.prefix}-${var.client}-${var.environment}-main-api-gateway"
  protocol_type = "HTTP"
  version       = "v1"
}

resource "aws_apigatewayv2_stage" "environment" {
  api_id = aws_apigatewayv2_api.main.id

  name        = var.environment
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


output "api_gateway_url" {
  value = aws_apigatewayv2_api.main.api_endpoint
}
