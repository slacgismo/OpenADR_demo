
# Define the tables and their schema
resource "aws_dynamodb_table" "devices" {
  name         = "${var.prefix}-${var.client}-${var.environment}-devices"
   billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  attribute {
    name = "device_id"
    type = "S"
  }

  hash_key = "device_id"
}

# Define second DynamoDB table
resource "aws_dynamodb_table" "orders" {
  name         = "${var.prefix}-${var.client}-${var.environment}-orders"
  billing_mode = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  attribute {
    name = "order_id"
    type = "S"
  }

  hash_key = "order_id"
}
# Define second DynamoDB table
resource "aws_dynamodb_table" "dispatches" {
  # name           = "battery-table"
  name           = "${var.prefix}-${var.client}-${var.environment}-dispatches"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "order_id"

  attribute {
    name = "order_id"
    type = "S"
  }

  tags = local.common_tags
}


resource "aws_dynamodb_table" "meters" {
  # name           = "battery-table"
  name           = "${var.prefix}-${var.client}-${var.environment}-meters"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "meter_id"

  attribute {
    name = "meter_id"
    type = "S"
  }

  tags = local.common_tags
}


locals {
  dispatch_json  = file("./templates/dump_dispatches.json")
  dispatch_data    = jsondecode(local.dispatch_json)

  order_json  = file("./templates/dump_orders.json")
  order_data    = jsondecode(local.order_json)

  devices_json  = file("./templates/dump_devices.json")
  devices_data    = jsondecode(local.devices_json)
}

# populate dynamodb table with data
resource "aws_dynamodb_table_item" "dispatches_table_item" {
  for_each = local.dispatch_data
  table_name = aws_dynamodb_table.dispatches.name
  hash_key   = "order_id"
  item = jsonencode(each.value)
}
resource "aws_dynamodb_table_item" "devices_table_item" {
  for_each = local.devices_data
  table_name = aws_dynamodb_table.devices.name
  hash_key   = "device_id"
  item = jsonencode(each.value)
}
resource "aws_dynamodb_table_item" "orders_table_item" {
  for_each = local.order_data
  table_name = aws_dynamodb_table.orders.name
  hash_key   = "order_id"
  item = jsonencode(each.value)
}

