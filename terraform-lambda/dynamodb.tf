
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
  attribute {
    name = "resource_id"
    type = "S"
  }

  hash_key = "market_id"

  global_secondary_index {
    name            = "resource_id-index"
    hash_key        = "resource_id"
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
  stream_view_type = "NEW_AND_OLD_IMAGES"

  hash_key = "device_id"
}

# Define Lambda function event trigger for DynamoDB
resource "aws_lambda_event_source_mapping" "dynamodb_event_source_mapping" {
  event_source_arn  = aws_dynamodb_table.devices.stream_arn
  function_name     = aws_lambda_function.lambda_dynamodb_event_trigger.arn
  starting_position = "LATEST"

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
    name = "resource_id"
    type = "S"
  }

  global_secondary_index {
    name               = "resource-device-index"
    hash_key           = "resource_id"
    range_key          = "device_id"
    projection_type    = "ALL"


    write_capacity     = 1
    read_capacity      = 1
  }
  tags = local.common_tags
}

