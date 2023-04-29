
# resource "aws_apigatewayv2_integration" "lambda_orders" {
#   api_id = aws_apigatewayv2_api.backend.id

#   integration_uri    = aws_lambda_function.lambda_orders.invoke_arn
#   integration_type   = "AWS_PROXY"
#   integration_method = "POST"
# }


# --------------------------------------------
#  ORDER "GET /db/orders"
# --------------------------------------------
# resource "aws_apigatewayv2_route" "query_orders" {
#   api_id = aws_apigatewayv2_api.backend.id

#   route_key = "GET /db/orders/query"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_orders.id}"
# }
# resource "aws_apigatewayv2_route" "scan_orders" {
#   api_id = aws_apigatewayv2_api.backend.id

#   route_key = "GET /db/orders/scan"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_orders.id}"
# }


# # --------------------------------------------
# #  ORDER "DELETE /db/orders"
# # --------------------------------------------
# resource "aws_apigatewayv2_route" "delete_orders" {
#   api_id = aws_apigatewayv2_api.backend.id

#   route_key = "DELETE /db/orders"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_orders.id}"
# }


# # --------------------------------------------
# #  ORDER "GET /db/order/{order_id}"
# # --------------------------------------------
# resource "aws_apigatewayv2_route" "get_an_order" {
#   api_id = aws_apigatewayv2_api.backend.id

#   route_key = "GET /db/order/{order_id}"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_orders.id}"
# }

# # --------------------------------------------
# #  Create an new order from device_id
# #  ORDER "POST /db/order" *Important*
# #  Submit an order from ven with device_id
# # --------------------------------------------
# resource "aws_apigatewayv2_route" "post_an_order" {
#   api_id    = aws_apigatewayv2_api.backend.id
#   route_key = "POST /db/order"
#   target = "integrations/${aws_apigatewayv2_integration.lambda_orders.id}"
# }

# # --------------------------------------------
# #  update order 
# #  ORDER "PUT /db/order/{order_id}
# # --------------------------------------------
# resource "aws_apigatewayv2_route" "put_an_order" {
#   api_id    = aws_apigatewayv2_api.backend.id
#   route_key = "PUT /db/order/{order_id}"
#   target = "integrations/${aws_apigatewayv2_integration.lambda_orders.id}"
# }



# # --------------------------------------------
# #  ORDER "DELETE /db/order/{order_id}"
# # --------------------------------------------
# resource "aws_apigatewayv2_route" "delete_an_order" {
#   api_id    = aws_apigatewayv2_api.backend.id
#   route_key = "DELETE /db/order/{order_id}"
#   # route_key = "POST /orders"
#   target = "integrations/${aws_apigatewayv2_integration.lambda_orders.id}"
# }

# resource "aws_lambda_permission" "api_gw_lambda_orders" {
#   statement_id  = "AllowExecutionFromAPIGateway-orders"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.lambda_orders.function_name
#   principal     = "apigateway.amazonaws.com"

#   source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
# }

