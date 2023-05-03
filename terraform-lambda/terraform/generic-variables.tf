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


# DynamoDB variables

variable "agents_table_name" {
  description = "agents_table_name"
  type       = string
}


variable "auctions_table_name" {
  description = "auctions_table_name"
  type       = string
}


variable "devices_table_name" {
  description = "devices_table_name"
  type       = string
}

variable "settings_table_name" {
  description = "settings_table_name"
  type       = string
}


variable "orders_table_name" {
  description = "orders_table_name"
  type       = string
}


variable "dispatches_table_name" {
  description = "dispatches_table_name"
  type       = string
}

variable "meters_table_name" {
  description = "meters_table_name"
  type       = string
}


variable "readings_table_name" {
  description = "readings_table_name"
  type       = string
}
variable "resources_table_name" {
  description = "resources_table_name"
  type       = string
}

variable "markets_table_name" {
  description = "markets_table_name"
  type       = string
}
variable "settlements_table_name" {
  description = "settlements_table_name"
  type       = string
}

variable "weather_table_name" {
  description = "weather_table_name"
  type       = string
}


# GSI info

variable "agents_gsi_info" {
  description = "agents_gsi_info"
  type       = string
}

variable "auctions_gsi_info" {
  description = "auctions_gsi_info"
  type       = string
}

variable "devices_gsi_info" {
  description = "devices_gsi_info"
  type       = string
}

variable "orders_gsi_info" {
  description = "orders_gsi_info"
  type       = string
}

variable "dispatches_gsi_info" {
  description = "dispatches_gsi_info"
  type       = string
}

variable "meters_gsi_info" {
  description = "meters_gsi_info"
  type       = string
}

variable "readings_gsi_info" {
  description = "readings_gsi_info"
  type       = string
}

variable "resources_gsi_info" {
  description = "resources_gsi_info"
  type       = string
}

variable "markets_gsi_info" {
  description = "markets_gsi_info"
  type       = string
}

variable "settings_gsi_info" {
  description = "settings_gsi_info"
  type       = string
}

variable "settlements_gsi_info" {
  description = "settlements_gsi_info"
  type       = string
}

variable "weather_gsi_info" {
  description = "weather_gsi_info"
  type       = string
}


# SQS  variables
variable "devices_settings_event_sqs_name" {
  description = "weather_table_name"
  type       = string
}


# S3 bucket
variable "meta_data_bucket_name" {
  description = "meta_data_bucket_name"
  type       = string
}










