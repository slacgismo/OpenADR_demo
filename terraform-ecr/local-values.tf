# Define Local Values in Terraform
locals {
  creator     = var.creator
  environment = var.environment
  name        = "${var.project}-${var.environment}"
  managedBy   = var.managedBy
  project     = var.project
  project_pa_number = var.project_pa_number
  #name = "${local.owners}-${local.environment}"
  common_tags = {
    creator     = local.creator
    managedBy   = local.managedBy
    environment = local.environment
    project     = local.project
    project-pa-number = local.project_pa_number
  }
} 