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
  description = "Agent definition file"
  type        = string
  # default     = "./templates/task-definition-agent.json.tpl"
}


variable "agent_id" {
  description = "The agent id"
}



# variable "ECSBackendDynamoDBLockName"{
#   description = "DynamoDB table name for Terraform remote backend lock of one ECS service (Agent))"
#   type        = string
#   # default     = "terraform-ecs-backend-lock"
# }




# variable "backend_s3_bucket_name" {
#   description = "The Terraform remote state backend S3 bucket name. This bucket is the same as the main deployment"
#   type        = string
# }

# variable "backend_s3_key" {
#   description = "The S3 state location. The key is the agent_id"
#   type        = string
# }

# variable "backend_dynamodb_table_name" {
#   description = "The backend of dynamodb state lock. the name is the agent_id"
#   type        = string
# }


# variable "tags" {
#   description = "Tages to set ECS services"
#   type        = map(string)
#   default     = {}
# }



# Input Variables
# AWS Region
# variable "aws_region" {
#   description = "Region in which AWS Resources to be created"
#   type        = string

# }

# ECS task defintions


# variable "prefix" {
#   description = "Prefix for all resources"
#   type        = string
# }