# Define Local Values in Terraform
locals {
  creator = var.creator
  environment = var.environment
  name = "${var.prefix}-${var.environment}"
  project = var.project
  common_tags = {
    creator = local.creator
    environment = local.environment
  }
} 