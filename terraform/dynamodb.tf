


resource "aws_dynamodb_table" "agenets_shared_state_lock" {
  name           = "${var.prefix}-${var.client}-${var.environment}-agent-shared-tf-state-lock"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = local.common_tags
}



# resource "aws_dynamodb_table" "mock_battery_table" {
#   # name           = "battery-table"
#   name           = "${var.prefix}-${var.client}-${var.environment}-mock-battery"
#   billing_mode   = "PROVISIONED"
#   read_capacity  = 1
#   write_capacity = 1
#   hash_key       = "serial"

#   attribute {
#     name = "serial"
#     type = "S"
#   }

#   tags = local.common_tags
# }


# #================================================================================================
# # Import battery data into dynamodb table
# #================================================================================================


# locals {
#   json_data  = file("./templates/lambda/batteries.json")
#   tf_data    = jsondecode(local.json_data)
# }


# # populate dynamodb table with data
# resource "aws_dynamodb_table_item" "dynamodb_schema_table_item" {
#   for_each = local.tf_data
#   table_name = aws_dynamodb_table.mock_battery_table.name
#   hash_key   = "serial"
#   item = jsonencode(each.value)
# }

# #================================================================================================
# # Output: DynamoDB Table for Agents Shared State Lock
# #================================================================================================


# output "dynamodb_agents_state_lock_table" {
#   value = aws_dynamodb_table.agenets_shared_state_lock.name
# }

