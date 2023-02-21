# Define Local Values in Terraform
locals {
  creator     = var.creator
  environment = var.environment
  name        = "${var.project}-${var.environment}"
  managedBy   = var.managedBy
  #name = "${local.owners}-${local.environment}"
  common_tags = {
    creator     = local.creator
    managedBy   = local.managedBy
    environment = local.environment
  }
} 