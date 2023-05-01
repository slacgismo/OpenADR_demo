# combine all openapi defintion files into one file
locals {
  depends_on = [aws_lambda_function.lambda_agents]

  # main openapi file
  openapi = jsondecode(file("${path.module}/api/openapi.json.tpl"))
  # agents openapi file
  agents_paths=  templatefile("${path.module}/api/agents/paths.json.tpl", {
    lambda_uri = aws_lambda_function.lambda_agents.invoke_arn
    timeoutInMillis = var.api_gateway_timeoutInMillis
  })
  agents_json = jsondecode(local.agents_paths)
  
  # auctions openapi file
  auctions_paths=  templatefile("${path.module}/api/auctions/paths.json.tpl", {
    lambda_uri = aws_lambda_function.lambda_auctions.invoke_arn
    timeoutInMillis = var.api_gateway_timeoutInMillis
  })
  auctions_json = jsondecode(local.auctions_paths)
  # devices openapi file
  devices_paths=  templatefile("${path.module}/api/devices/paths.json.tpl", {
    lambda_uri = aws_lambda_function.lambda_devices.invoke_arn
    timeoutInMillis = var.api_gateway_timeoutInMillis
  })
  devices_json = jsondecode(local.devices_paths)
  # dispatches openapi file
  dispatches_paths=  templatefile("${path.module}/api/dispatches/paths.json.tpl", {
    lambda_uri = aws_lambda_function.dispatches.invoke_arn
    timeoutInMillis = var.api_gateway_timeoutInMillis
  })
  dispatches_json = jsondecode(local.dispatches_paths)


  # markets openapi file
  markets_paths=  templatefile("${path.module}/api/markets/paths.json.tpl", {
    lambda_uri = aws_lambda_function.lambda_markets.invoke_arn
    timeoutInMillis = var.api_gateway_timeoutInMillis
  })
  markets_json = jsondecode(local.markets_paths)


  # meters openapi file
  meters_paths=  templatefile("${path.module}/api/meters/paths.json.tpl", {
    lambda_uri = aws_lambda_function.lambda_meters.invoke_arn
    timeoutInMillis = var.api_gateway_timeoutInMillis
  })
  meters_json = jsondecode(local.meters_paths)

    # meters openapi file
  orders_paths=  templatefile("${path.module}/api/orders/paths.json.tpl", {
    lambda_uri = aws_lambda_function.lambda_orders.invoke_arn
    timeoutInMillis = var.api_gateway_timeoutInMillis
  })
  orders_json = jsondecode(local.orders_paths)
  
  # readings openapi file
  readings_paths=  templatefile("${path.module}/api/readings/paths.json.tpl", {
    lambda_uri = aws_lambda_function.lambda_readings.invoke_arn
    timeoutInMillis = var.api_gateway_timeoutInMillis
  })
  readings_json = jsondecode(local.readings_paths)

  # resources openapi file
  resources_paths=  templatefile("${path.module}/api/resources/paths.json.tpl", {
    lambda_uri = aws_lambda_function.lambda_resources.invoke_arn
    timeoutInMillis = var.api_gateway_timeoutInMillis
  })
  resources_json = jsondecode(local.resources_paths)

  # settings openapi file
  settings_paths=  templatefile("${path.module}/api/settings/paths.json.tpl", {
    lambda_uri = aws_lambda_function.lambda_settings.invoke_arn
    timeoutInMillis = var.api_gateway_timeoutInMillis
  })
  settings_json = jsondecode(local.settings_paths)

  # settlements openapi file
  settlements_paths=  templatefile("${path.module}/api/settlements/paths.json.tpl", {
    lambda_uri = aws_lambda_function.lambda_settlements.invoke_arn
    timeoutInMillis = var.api_gateway_timeoutInMillis
  })
  settlements_json = jsondecode(local.settlements_paths)

  # weather openapi file
  weather_paths=  templatefile("${path.module}/api/weather/paths.json.tpl", {
    lambda_uri = aws_lambda_function.lambda_weather.invoke_arn
    timeoutInMillis = var.api_gateway_timeoutInMillis
  })
  weather_json = jsondecode(local.weather_paths)
  
  # swagger openapi file
  # swagger_paths=  templatefile("${path.module}/api/swagger/paths.json.tpl", {
  #   lambda_uri = aws_lambda_function.lambda_swagger.invoke_arn
  #   timeoutInMillis = var.api_gateway_timeoutInMillis
  # })
  # swagger_json = jsondecode(local.swagger_paths)
  # combine all paths
  combined_paths = merge(
    local.openapi.paths, 
    local.agents_json.paths,
    local.auctions_json.paths,
    local.devices_json.paths,
    local.dispatches_json.paths,
    local.markets_json.paths,
    local.meters_json.paths,
    local.orders_json.paths,
    local.readings_json.paths,
    local.resources_json.paths,
    local.settings_json.paths,
    local.settlements_json.paths,
    local.weather_json.paths,
    # local.swagger_json.paths
    ) 
  combined_openapi = merge(local.openapi, { "paths": local.combined_paths })
  combined_openapi_json = jsonencode(local.combined_openapi)
}

# export the openapi file
resource "local_file" "openapi_json" {
  content  = local.combined_openapi_json
  filename = "${path.module}/api/openapi.json"
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
