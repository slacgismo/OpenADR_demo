# Input Variables
# AWS Region
variable "aws_region" {
  description = "Region in which AWS Resources to be created"
  type        = string
  default     = "us-east-2"
}
# Environment Variable
variable "environment" {
  description = "Environment Variable used as a prefix"
  type        = string
  default     = "dev"
}

variable "project" {
  description = "project name"
  type        = string
  default     = "TESS"
}
variable "prefix" {
  description = "Name prefix"
  type        = string
  default     = "openadr"
}
variable "creator" {
  description = "Creator"
  type        = string
  default     = "Jimmy Leu"
}
variable "managedBy" {
  description = "Managed by"
  type        = string
  default     = "Terraform"
}


# from terraform.tfvars
variable "meter_api_url" {
  description = "save data url"
  type        = string
}
variable "device_api_url" {
  description = "get vens url"
  type        = string
}
variable "order_api_url" {
  description = "market prices url"
  type        = string
}
variable "dispatch_api_url" {
  description = "participated vens url"
  type        = string
}
variable "emulated_device_api_url" {
  description = "mock devices api url"
  type        = string
}
variable "vtn_address" {
  description = "vtn address"
  type        = string
  default     = "localhost"
}
variable "vtn_port" {
  description = "vtn port"
  type        = string
  default     = "8000"
}

variable "app_image_vtn" {
  description = "app_image_vtn"
  type        = string
}

variable "app_image_ven" {
  description = "app_image_vtn"
  type        = string
}

variable "devices_worker_health_check_port" {
  type        = string
  description = "The name of the file containing the devices worker task definition"
  default     = "8070"
}



variable "device_worker_role_name" {
  default = "devices-workers-roles"
}

variable "backend_main_s3_bucket" {
  description = "The name of the S3 bucket where the Terraform state file will be stored"
}

variable "backend_main_s3_key" {
  description = "The name of the S3 object where the Terraform state file will be stored"
}

variable "backend_main_s3_region" {
  description = "The AWS region where the S3 bucket where the Terraform state file will be stored"
}


variable "backend_dynamodb_table" {
  description = "The name of the DynamoDB table that will be used to lock the state file when running Terraform"
}

variable "app_image_device_worker" {
  description = "The ecr image of deivce worker"
}

variable "app_image_device_cli" {
  description = "The ecr image of deivce cli"
}