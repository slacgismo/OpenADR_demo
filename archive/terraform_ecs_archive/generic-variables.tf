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



