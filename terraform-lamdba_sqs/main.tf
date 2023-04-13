# Terraform Block

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }

  }
}

provider "aws" {
  region = var.aws_region
}



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
  description = "project name"
  type        = string
  default     = "20813-H2002"
}


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