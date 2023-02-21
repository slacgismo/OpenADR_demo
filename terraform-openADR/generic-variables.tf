

# Input Variables
# AWS Region
variable "aws_region" {
  description = "Region in which AWS Resources to be created"
  type = string
  default = "us-east-2"  
}
# Environment Variable
variable "environment" {
  description = "Environment Variable used as a prefix"
  type = string
  default = "dev"
}
# Project name
variable "project" {
  description = "Project name"
  type = string
  default = "TESS"
}

# Prefix
variable "prefix" {
  description = "Prefix name"
  type = string
  default = "openadr"
}

variable "creator" { 
  description = "Creator of this project"
  type = string
  default = "Jimmy Leu"
}