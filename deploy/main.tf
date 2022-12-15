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
  version = "~> 2.50.0"
}
