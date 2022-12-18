terraform {
  backend "s3" {
    bucket         = "openadr-devops-tfstate"
    key            = "openadr.tfstate"
    region         = "us-east-2"
    encrypt        = true
    dynamodb_table = "openadr-devops-tf-state-lock"
  }
}

provider "aws" {
  region = "us-east-2"
  #   version = "~> 4.47.0"
}


locals {
  prefix = "${var.prefix}-${terraform.workspace}"
}


locals {
  common_tags = {
    Environment = terraform.workspace
    Project     = var.project
    Owner       = var.contact
    ManagedBy   = "Terraform"
  }
}


data "aws_region" "current" {}