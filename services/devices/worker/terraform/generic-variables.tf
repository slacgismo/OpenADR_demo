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


variable "task_definition_file" {
  description = "task definition file. this variable is import from python script"
  type        = string
  # default     = "./templates/task-definition-agent.json.tpl"
}


variable "agent_id" {
  description = "The agent id"
}

# variable from terraform.tfvars
variable "METER_API_URL"  {
  description = "Save data url"
  type        = string

}

variable "DISPATCH_API_URL"  {
  description = "participated vens url"
  type        = string

}

variable "DEVICE_API_URL"  {
  description = "get vens url"
  type        = string
}

variable "app_image_vtn"  {
  description = "app image vtn"
  type        = string
}

variable "app_image_ven"  {
  description = "app image ven"
  type        = string
}


variable "EMULATED_DEVICE_API_URL"  {
  description = "mock devices api url"
  type        = string
}
variable "ORDER_PAI_URL"  {
  description = "market prices url"
  type        = string
}

variable "vtn_address"  {
  description = "vtn address"
  type        = string
}

variable "vtn_port"  {
  description = "vtn port"
  type        = string
}


