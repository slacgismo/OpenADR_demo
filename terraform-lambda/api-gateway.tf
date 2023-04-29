# combine all openapi defintion files into one file
locals {
  depends_on = [aws_lambda_function.lambda_agents]
  openapi = jsondecode(file("${path.module}/api/openapi.json.tpl"))
  agents_query_path=  templatefile("${path.module}/api/agents/paths.json.tpl", {
    lambda_uri = aws_lambda_function.lambda_agents.invoke_arn
    timeoutInMillis = 2900
  })
  agents_json = jsondecode(local.agents_query_path)
  
  # agents_paths = jsondecode(file("${path.module}/api/agents/paths.json"))
  # auctions_paths = jsondecode(file("${path.module}/api/auctions/paths.json"))
  combined_paths = merge(
    local.openapi.paths, 
    local.agents_json.paths,
    # local.auctions_paths.paths
    ) 
  combined_openapi = merge(local.openapi, { "paths": local.combined_paths })
  combined_openapi_json = jsonencode(local.combined_openapi)
}

resource "aws_apigatewayv2_api" "backend" {
  depends_on = [aws_lambda_function.lambda_agents]
  name          ="${var.prefix}-${var.client}-${var.environment}-backend-api-gateway"
  protocol_type = "HTTP"
  description  =  "Backend API Gateway"
  body = local.combined_openapi_json
  tags = local.common_tags
}

# output "openapi" {
#   value = local.combined_openapi_json
# }

# resource "aws_apigatewayv2_deployment" "main" {
#   depends_on =  [aws_lambda_function.lambda_agents]
#   api_id      = aws_apigatewayv2_api.backend.id
#   description = "Initial deployment"
#   lifecycle {
#     create_before_destroy = true
#   }
  
# }



resource "aws_apigatewayv2_stage" "environment" {
  api_id = aws_apigatewayv2_api.backend.id

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
  name = "/aws/api-gw/${aws_apigatewayv2_api.backend.name}"

  retention_in_days = 14
  tags = local.common_tags
}


output "api_gateway_url" {
  value = aws_apigatewayv2_api.backend.api_endpoint
}
