
# Markets

resource "aws_dynamodb_table" "markets" {
  name           = "${var.prefix}-${var.client}-${var.environment}-markets"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  attribute {
    name = "market_id"
    type = "S"
  }

  hash_key = "market_id"
}


# Resources

resource "aws_dynamodb_table" "resources" {
  name           = "${var.prefix}-${var.client}-${var.environment}-resources"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  attribute {
    name = "resource_id"
    type = "S"
  }

  hash_key = "resource_id"
}


# Agents

resource "aws_dynamodb_table" "agents" {
  name           = "${var.prefix}-${var.client}-${var.environment}-agents"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  attribute {
    name = "agent_id"
    type = "S"
  }

  hash_key = "agent_id"
}


# Devices
resource "aws_dynamodb_table" "devices" {
  name           = "${var.prefix}-${var.client}-${var.environment}-devices"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  attribute {
    name = "device_id"
    type = "S"
  }
  # enable the dynamondb stream to trigger the event sqs queue
  stream_enabled = true
  stream_view_type = "NEW_IMAGE"

  hash_key = "device_id"
}

# Define Lambda function event trigger for DynamoDB
resource "aws_lambda_event_source_mapping" "dynamodb_event_source_mapping" {
  event_source_arn  = aws_dynamodb_table.devices.stream_arn
  function_name     = aws_lambda_function.lambda_dynamodb_event_trigger.arn
  starting_position = "LATEST"

}

# Orders
# Define second DynamoDB table
resource "aws_dynamodb_table" "orders" {
  name           = "${var.prefix}-${var.client}-${var.environment}-orders"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1

  attribute {
    name = "order_id"
    type = "S"
  }

  attribute {
    name = "device_id"
    type = "S"
  }

  hash_key = "order_id"

  global_secondary_index {
    name            = "device_id-index"
    hash_key        = "device_id"
    range_key       = "order_id"
    projection_type = "ALL"
    read_capacity   = 1
    write_capacity  = 1
  }
}
# Dispatches

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


# locals {
#   dispatch_json = file("./templates/dump_dispatches.json")
#   dispatch_data = jsondecode(local.dispatch_json)

#   order_json = file("./templates/dump_orders.json")
#   order_data = jsondecode(local.order_json)

#   devices_json = file("./templates/dump_devices.json")
#   devices_data = jsondecode(local.devices_json)
# }

# # populate dynamodb table with data
# resource "aws_dynamodb_table_item" "dispatches_table_item" {
#   for_each   = local.dispatch_data
#   table_name = aws_dynamodb_table.dispatches.name
#   hash_key   = "order_id"
#   item       = jsonencode(each.value)
# }


# resource "aws_dynamodb_table_item" "devices_table_item" {
#   for_each   = local.devices_data
#   table_name = aws_dynamodb_table.devices.name
#   hash_key   = "device_id"
#   item       = jsonencode(each.value)
# }

# resource "aws_dynamodb_table_item" "orders_table_item" {
#   for_each   = local.order_data
#   table_name = aws_dynamodb_table.orders.name
#   hash_key   = "order_id"
#   item       = jsonencode(each.value)
# }

