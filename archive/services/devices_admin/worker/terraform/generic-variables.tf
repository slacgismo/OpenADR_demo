# Input Variables
# AWS Region
variable "aws_region" {
  description = "Region in which AWS Resources to be created"
  type        = string
  # default     = "us-east-2"
}
# Environment Variable
variable "environment" {
  description = "Environment Variable used as a prefix"
  type        = string
  # default     = "dev"
}

variable "project" {
  description = "project name"
  type        = string
  # default     = "TESS"
}
variable "prefix" {
  description = "Name prefix"
  type        = string
  # default     = "openadr"
}
variable "creator" {
  description = "Creator"
  type        = string
  # default     = "Jimmy Leu"
}
variable "managedBy" {
  description = "Managed by"
  type        = string
  # default     = "Terraform"
}


variable "backend_dyanmodb_table_teraform_state_lock_devices_admin"{
  description = "DynamoDB table name for Terraform remote backend lock of one ECS service (Agent)). This variable is import from python script."
  type        = string
  # default     = "terraform-ecs-backend-lock"
}


variable "backend_s3_bucket_devices_admin"{
  description = "bacend s3 bucket name for devices admin"
  type        = string
}