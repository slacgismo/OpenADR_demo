resource "aws_dynamodb_table" "terraform_state_lock_table" {
 # Only create the table if the iscreated variable is true

  name           = var.ECSBackendDynamoDBLockName
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