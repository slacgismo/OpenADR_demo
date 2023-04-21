variable "lambda_function_name" {
  description = "Name of the lambda function"
  type        = string
}


variable "lambda_function_path" {
  description = "Path of the lambda function"
  type        = string
}

variable "lambda_function_handler" {
  description = "Handler of the lambda function"
  type        = string
}

variable "lambda_log_retention_in_days" {
    description = "Retention of the cloudwatch logs"
    type        = number
}
variable "lambda_function_runtime" {
  description = "Runtime of the lambda function"
  type        = string
}

variable "lambda_function_memory_size" {
  description = "Memory size of the lambda function"
  type        = number
}

variable "lambda_function_s3_bucket_id" {
  description = "S3 bucket of the lambda function zip file"
  type        = string
}


variable "lambda_environment_variables" {
  description = "Environment variables to set on the lambda function"
  type        = map(string)
  default     = {}
}


variable "s3_policy_arn" {
  description = "S3 policy to attach to the lambda function"
  type        = string
}

variable "dynamodb_policy_arn" {
  description = "dynamodb policy to attach to the lambda function"
  type        = string
}

variable "timestream_policy_arn" {
  description = "timestream policy to attach to the lambda function"
  type        = string
}

variable "tags" {
  description = "Tages to set on the bucket"
  type        = map(string)
  default     = {}
}