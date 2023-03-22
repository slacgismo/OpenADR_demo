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
variable "save_data_url" {
  description = "save data url"
  type        = string
}
variable "get_vens_url" {
  description = "get vens url"
  type        = string
}
variable "market_prices_url" {
  description = "market prices url"
  type        = string
}
variable "participated_vens_url" {
  description = "participated vens url"
  type        = string
}
variable "mock_devices_api_url" {
  description = "mock devices api url"
  type        = string
}
variable "vtn_address" {
  description = "vtn address"
  type        = string
}
variable "vtn_port" {
  description = "vtn port"
  type        = string
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
  default     = 8070
}
