


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

output "dynamodb_agents_state_lock_table" {
  value = aws_dynamodb_table.agenets_shared_state_lock.name
}

