# create a dynamodb table that will be used to store the agents \
# and their terraform state lock , terraform s3 state key, and \
# task definition file location

resource "aws_dynamodb_table" "agents-table" {
  name           = "${var.prefix}-agents-table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "agent_id"

  attribute {
    name = "agent_id"
    type = "S"
  }

  tags = local.common_tags
}


resource "aws_dynamodb_table" "agenets_state_lock" {
  name           = "${var.prefix}-devices-admin-tf-state-lock"
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

output "dynamodb_agents_state_lock_table" {
    value = aws_dynamodb_table.agenets_state_lock.name
}

output "dynamodb_agent_table" {
    value = aws_dynamodb_table.agents-table.name
}