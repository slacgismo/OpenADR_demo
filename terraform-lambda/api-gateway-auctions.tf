
# resource "aws_apigatewayv2_integration" "lambda_auctions" {
#   api_id = aws_apigatewayv2_api.backend.id

#   integration_uri    = aws_lambda_function.lambda_auctions.invoke_arn
#   integration_type   = "AWS_PROXY"
#   integration_method = "POST"
# }

# --------------------------------------------
# AUCTION "GET /db/auctions/{market_id}"
# --------------------------------------------

# resource "aws_apigatewayv2_route" "query_list_of_auctions" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "GET /db/auctions/query"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_auctions.id}"
# }

# resource "aws_apigatewayv2_route" "scan_auctions" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "GET /db/auctions/scan"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_agents.id}"
# }




# --------------------------------------------
# AUCTION "POST /db/auctions"
# --------------------------------------------
# resource "aws_apigatewayv2_route" "post_list_of_auctions_from_market_id" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "POST /db/auctions"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_auctions.id}"
# }
# --------------------------------------------
# AUCTION "PUT /db/auctions"
# no need for put multiple auctions
# --------------------------------------------

# --------------------------------------------
# AUCTION "DELETE /db/auctions"
# --------------------------------------------

# resource "aws_apigatewayv2_route" "delete_list_of_auctions_from_market_id" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "DELETE /db/auctions"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_auctions.id}"
# }



# --------------------------------------------
# AUCTION "GET /db/auction/{auction_id}"
# --------------------------------------------

# resource "aws_apigatewayv2_route" "get_a_auction" {
#   api_id = aws_apigatewayv2_api.backend.id
#   route_key = "GET /db/auction/{auction_id}"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda_auctions.id}"
# }

# --------------------------------------------
# Update auction
# AUCTION "POST /db/auction/{auction_id}"
# --------------------------------------------

# resource "aws_apigatewayv2_route" "post_a_auction" {
#  # Put an agent record to table
#   api_id    = aws_apigatewayv2_api.backend.id
#   route_key = "POST /db/auction"

#   target = "integrations/${aws_apigatewayv2_integration.lambda_auctions.id}"
# }


# --------------------------------------------
# Update auction
# AUCTION "PUT /db/auction/{auction_id}"
# --------------------------------------------

# resource "aws_apigatewayv2_route" "put_a_auction" {
#  # Put an agent record to table
#   api_id    = aws_apigatewayv2_api.backend.id
#   route_key = "PUT /db/auction/{auction_id}"

#   target = "integrations/${aws_apigatewayv2_integration.lambda_auctions.id}"
# }

# --------------------------------------------
# Update auction
# AUCTION "DELETE /db/auction/{auction_id}"
# --------------------------------------------
# resource "aws_apigatewayv2_route" "delete_a_auction" {
#   api_id    = aws_apigatewayv2_api.backend.id
#   route_key = "DELETE /db/auction/{auction_id}"
#   target = "integrations/${aws_apigatewayv2_integration.lambda_auctions.id}"
# }

# resource "aws_lambda_permission" "api_gw_lambda_auctions" {
#   statement_id  = "AllowExecutionFromAPIGateway-auctions"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.lambda_auctions.function_name
#   principal     = "apigateway.amazonaws.com"

#   source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
# }

