
# Markets

resource "aws_dynamodb_table" "markets" {
  name           = "${var.prefix}-${var.client}-${var.environment}-markets"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key = "market_id"

  attribute {
    name = "market_id"
    type = "S"
  }
  attribute {
    name = "resource_id"
    type = "S"
  }
  attribute{
    name = "market_status"
    type = "N"
  }
  attribute {
    name = "valid_at"
    type = "N"
  }

  # query market_id from resource_id and valid_at > timestampe

  global_secondary_index {
    name            = "resource_id_valid_at_index"
    hash_key        = "resource_id"
    range_key       = "valid_at"
    projection_type = "ALL"
    read_capacity   = 1
    write_capacity  = 1
  }

  global_secondary_index {
    name            = "market_status_valid_at_index"
    hash_key        = "market_status"
    range_key       = "valid_at"
    projection_type = "ALL"
    read_capacity   = 1
    write_capacity  = 1
  }
  tags = local.common_tags
}


# Resources

resource "aws_dynamodb_table" "resources" {
  name           = "${var.prefix}-${var.client}-${var.environment}-resources"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key = "resource_id"
  attribute {
    name = "resource_id"
    type = "S"
  }
  attribute {
    name = "resource_status"
    type = "N"
  }

  attribute {
    name = "valid_at"
    type = "N"
  }
  global_secondary_index {
    name            = "resource_status_valid_at_index"
    hash_key        = "resource_status"
    range_key       = "valid_at"
    projection_type = "ALL"
    read_capacity   = 1
    write_capacity  = 1
  }
  tags = local.common_tags
}


# Agents

resource "aws_dynamodb_table" "agents" {
  name           = "${var.prefix}-${var.client}-${var.environment}-agents"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key = "agent_id"
  
  attribute {
    name = "agent_id"
    type = "S"
  }

  attribute {
    name = "resource_id"
    type = "S"
  }

  attribute {
    name = "valid_at"
    type = "N"
  }

  # query agent_id from resource_id and valid_at > timestampe
  global_secondary_index {
    name            = "resource_id_valid_at_index"
    hash_key        = "resource_id"
    range_key       = "valid_at"
    projection_type = "ALL"
    read_capacity   = 1
    write_capacity  = 1
  }
}


# Devices
resource "aws_dynamodb_table" "devices" {
  name           = "${var.prefix}-${var.client}-${var.environment}-devices"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key = "device_id"

  attribute {
    name = "device_id"
    type = "S"
  }
  # enable the dynamondb stream to trigger the event sqs queue
  stream_enabled = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

 
  attribute {
    name = "valid_at"
    type = "N"
  }
  attribute {
    name = "device_status"
    type = "N"
  }
  attribute {
    name = "agent_id"
    type = "S"
  }

  # query device_id from agent_id and valid_at > timestampe
  global_secondary_index {
    name            = "agent_id_valid_at_index"
    hash_key        = "agent_id"
    range_key       = "valid_at"
    projection_type = "ALL"
    read_capacity   = 1
    write_capacity  = 1
  }
  global_secondary_index {
    name            = "device_status_valid_at_index"
    hash_key        = "device_status"
    range_key       = "valid_at"
    projection_type = "ALL"
    read_capacity   = 1
    write_capacity  = 1
  }
}

# Define Lambda function event trigger for DynamoDB
resource "aws_lambda_event_source_mapping" "devices_event_source_mapping" {
  event_source_arn  = aws_dynamodb_table.devices.stream_arn
  function_name     = aws_lambda_function.lambda_dynamodb_event_trigger.arn
  starting_position = "LATEST"

}

# Auctions

resource "aws_dynamodb_table" "auctions" {
  name           = "${var.prefix}-${var.client}-${var.environment}-auctions"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key = "auction_id"

  attribute {
    name = "auction_id"
    type = "S"
  }

  attribute {
    name = "market_id"
    type = "S"
  }

  attribute {
    name = "valid_at"
    type = "N"
  }

  # query auction_id from market_id and valid_at > timestampe
  global_secondary_index {
    name            = "market_id_valid_at_index"
    hash_key        = "market_id"
    range_key       = "valid_at"
    projection_type = "ALL"
    read_capacity   = 1
    write_capacity  = 1
  }
}

# Orders

resource "aws_dynamodb_table" "orders" {
  name           = "${var.prefix}-${var.client}-${var.environment}-orders"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key = "order_id"

  attribute {
    name = "order_id"
    type = "S"
  }

  attribute {
    name = "device_id"
    type = "S"
  }
  
  attribute {
    name = "valid_at"
    type = "N"
  }

  
  global_secondary_index {
    name            = "device_id_order_id_index"
    hash_key        = "device_id"
    range_key       = "order_id"
    projection_type = "ALL"
    read_capacity   = 1
    write_capacity  = 1
  }

  global_secondary_index {
    name            = "order_id_valid_at_index"
    hash_key        = "order_id"
    range_key       = "valid_at"
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

  attribute {
    name = "valid_at"
    type = "N"
  }

  global_secondary_index {
    name            = "order_id_valid_at_index"
    hash_key        = "order_id"
    range_key       = "valid_at"
    projection_type = "ALL"
    read_capacity   = 1
    write_capacity  = 1
  }
  tags = local.common_tags
}

# Meters
resource "aws_dynamodb_table" "meters" {
  name           = "${var.prefix}-${var.client}-${var.environment}-meters"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1

  hash_key = "meter_id"

  attribute {
    name = "meter_id"
    type = "S"
  }

  attribute {
    name = "device_id"
    type = "S"
  }
  attribute {
    name = "meter_status"
    type = "N"
  }
  attribute {
    name = "resource_id"
    type = "S"
  }
  attribute {
    name = "valid_at"
    type = "N"
  }

  global_secondary_index {
    name               = "resource_id_device_id_index"
    hash_key           = "resource_id"
    range_key          = "device_id"
    projection_type    = "ALL"
    write_capacity     = 1
    read_capacity      = 1
  }

  global_secondary_index {
    name               = "meter_status_valid_at_index"
    hash_key           = "meter_status"
    range_key          = "valid_at"
    projection_type    = "ALL"
    write_capacity     = 1
    read_capacity      = 1
  }
  tags = local.common_tags
}

# Settings
resource "aws_dynamodb_table" "settings" {
  name           = "${var.prefix}-${var.client}-${var.environment}-settings"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "setting_id"

  attribute {
    name = "setting_id"
    type = "S"
  }

  attribute {
    name = "device_id"
    type = "S"
  }

  attribute {
    name = "valid_at"
    type = "N"
  }

  global_secondary_index {
    name            = "device_id_valid_at_index"
    hash_key        = "device_id"
    range_key       = "valid_at"
    projection_type = "ALL"
    read_capacity   = 1
    write_capacity  = 1
  }

  # enable the dynamondb stream to trigger the event sqs queue
  stream_enabled = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  tags = local.common_tags
}

# Define Lambda function event trigger for DynamoDB
# resource "aws_lambda_event_source_mapping" "settings_event_source_mapping" {
#   event_source_arn  = aws_dynamodb_table.settings.stream_arn
#   function_name     = aws_lambda_function.lambda_dynamodb_event_trigger.arn
#   starting_position = "LATEST"

# }


# Readings
resource "aws_dynamodb_table" "readings" {
  name           = "${var.prefix}-${var.client}-${var.environment}-readings"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "reading_id"

  attribute {
    name = "reading_id"
    type = "S"
  }

  attribute {
    name = "meter_id"
    type = "S"
  }

  attribute {
    name = "valid_at"
    type = "N"
  }



  global_secondary_index {
    name            = "meter_id_index"
    hash_key        = "meter_id"
    projection_type = "ALL"
    read_capacity   = 1
    write_capacity  = 1
  }

  global_secondary_index {
    name            = "meter_id_valid_at_index"
    hash_key        = "meter_id"
    range_key       = "valid_at"
    projection_type = "ALL"
    read_capacity   = 1
    write_capacity  = 1
  }

  tags = local.common_tags
}

# Settlements
resource "aws_dynamodb_table" "settlements" {
  name           = "${var.prefix}-${var.client}-${var.environment}-settlements"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "order_id"

  attribute {
    name = "order_id"
    type = "S"
  }


  attribute {
    name = "valid_at"
    type = "N"
  }

  global_secondary_index {
    name            = "order_id_valid_at_index"
    hash_key        = "order_id"
    range_key       = "valid_at"
    projection_type = "ALL"
    read_capacity   = 1
    write_capacity  = 1
  }
  tags = local.common_tags
}

# Weather
resource "aws_dynamodb_table" "weather" {
  name           = "${var.prefix}-${var.client}-${var.environment}-weather"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "weather_id"

  attribute {
    name = "weather_id"
    type = "S"
  }

  attribute {
    name = "zip_code"
    type = "S"
  }
  attribute {
    name = "valid_at"
    type = "N"
  }

  global_secondary_index {
    name            = "zip_code_valid_at_index"
    hash_key        = "zip_code"
    range_key       = "valid_at"
    projection_type = "ALL"
    read_capacity   = 1
    write_capacity  = 1
  }


  tags = local.common_tags
}

# ==================================
# dump json file to dynamodb exmaple
# ==================================

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

