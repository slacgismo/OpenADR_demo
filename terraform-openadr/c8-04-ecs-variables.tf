# ECS  Variables
## VEN variables


variable "ecr_image_ven" {
  description = "ecr_image_ven"
  type        = string
  default    = "041414866712.dkr.ecr.us-east-2.amazonaws.com/ven:latest"
}

variable "mock_battery_api_url" {
  description = "mock_battery_api_url"
  type        = string
  default    = "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/battery_api"
}

# variable "dev" {
#   description = "dev"
#   type        = string
#   default    = true
# }

    # mock_battery_api_url = var.mock_battery_api_url
    # battery_token    = var.battery_token
    # battery_sn       = var.battery_sn
    # device_id        = var.device_id
    # device_type      = var.device_type
    # timezone         = var.timezone
    # price_threshold  = var.price_threshold
    # log_group_name   = aws_cloudwatch_log_group.ven_task_logs.name
    # log_group_region = var.aws_region

## VTN variables

# ecr image vtn name

variable "ecr_image_vtn" {
  description = "ecr_image_vtn"
  type        = string
  default    = "041414866712.dkr.ecr.us-east-2.amazonaws.com/vtn:latest"
}
# timezone
variable "timezone" {
  description = "timezone"
  type        = string
  default  = "America/Los_Angeles"
}
# save data url of an api gateway endpoint
variable "save_data_url" {
  description = "save_data_url"
  type        = string
  # replace with generated api gateway endpoint url when we combine all the services
  default = "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
}

# participate vens url of an api gateway endpoint
variable "get_vens_url" {
  description = "get_vens_url"
  type        = string
  # replace with generated api gateway endpoint url when we combine all the services
  default = "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
}



# marker prices url of an api gateway endpoint
variable "market_prices_url" {
  description = "market_prices_url"
  type        = string
    # replace with generated api gateway endpoint url when we combine all the services
  default = "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/market_prices"
}


# participate vens url of an api gateway endpoint
variable "participated_vens_url" {
  description = "participated_vens_url"
  type        = string
  # replace with generated api gateway endpoint url when we combine all the services
  default = "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/participated_vens"
}




