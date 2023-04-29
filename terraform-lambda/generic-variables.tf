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
  default     = "STAGING"
}
variable "client" {
  description = "Client name"
  type        = string
  default     = "NHEC"
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



variable "project_pa_number" {
  description = "project pa bumber"
  type        = string
  default     = "20813-H2002"
}


variable "api_version" {
  description = "api version"
  type        = string
  default     = "v1"
}

variable "api_gateway_timeoutInMillis" {
  description = "api gateway timeoutInMillis"
  type        = string
  default     = "29000"
}