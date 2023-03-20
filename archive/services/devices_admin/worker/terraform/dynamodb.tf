data "templates" "tables_file" {
  template = file("${path.module}/templates/${var.dynamodb_table_lock_list_file_name}")
}

locals {
  tables = jsondecode(data.templates.tables_file.rendered).tables
}

resource "aws_dynamodb_table" "dynamodb_tables" {
  for_each = { for t in local.tables : t.table_name => t }

  name = each.key
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


# resource "aws_dynamodb_table" "terraform_state_lock_table" {
#  # Only create the table if the iscreated variable is true

#   name           = var.backend_dyanmodb_table_teraform_state_lock_devices_admin
#   billing_mode   = "PROVISIONED"
#   read_capacity  = 1
#   write_capacity = 1
#   hash_key       = "LockID"

#   attribute {
#     name = "LockID"
#     type = "S"
#   }

#   tags = local.common_tags
# }