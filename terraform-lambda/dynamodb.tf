resource "aws_dynamodb_table" "battery-table" {
  # name           = "battery-table"
  name           = "${var.prefix}-${var.client}-${var.environment}-mock-battery"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "serial"

  attribute {
    name = "serial"
    type = "S"
  }

  tags = local.common_tags
}

# read json file
locals {
  json_data  = file("./batteries.json")
  tf_data    = jsondecode(local.json_data)
}


# populate dynamodb table with data
resource "aws_dynamodb_table_item" "dynamodb_schema_table_item" {
  for_each = local.tf_data
  table_name = aws_dynamodb_table.battery-table.name
  hash_key   = "serial"
  item = jsonencode(each.value)
}



