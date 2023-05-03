# Input Variables
# AWS Region
variable "aws_region" {
  description = "Region in which AWS Resources to be created"
  type        = string

}
# Environment Variable
variable "environment" {
  description = "Environment Variable used as a prefix"
  type        = string

}
variable "client" {
  description = "Client name"
  type        = string

}

variable "project" {
  description = "project name"
  type        = string

}
variable "prefix" {
  description = "Name prefix"
  type        = string

}
variable "creator" {
  description = "Creator"
  type        = string
}
variable "managedBy" {
  description = "Managed by"
  type        = string

}



variable "project_pa_number" {
  description = "project pa bumber"
  type        = string
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


