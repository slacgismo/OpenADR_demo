# Define Local Values in Terraform
locals {
  creator     = var.creator
  environment = var.environment
  name        = "${var.project}-${var.environment}"
  managedBy   = var.managedBy
  project     = var.project
  project_pa_number = var.project_pa_number
  ecr_image_tag = "latest"
  account_id    = data.aws_caller_identity.current.account_id
  #name = "${local.owners}-${local.environment}"
  common_tags = {
    creator     = local.creator
    managedBy   = local.managedBy
    environment = local.environment
    project     = local.project
    project-pa-number = local.project_pa_number
  }
}



