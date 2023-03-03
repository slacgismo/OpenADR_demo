# ECS  Variables
## VEN variables

# define if this ven to use mock battery api
variable "dev" {
  description = "VEN dev"
  default = "True"
}

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


variable "ven_log_group_name" {
  description = "ven_log_group_name"
  type        = string
  default    = "ven"
}


## VTN variables
variable "vtn_id" {
  description = "vtn_id"
  type        = string
  default    = "vtn0"
}
# ecr image vtn name
variable "interval_of_fetching_market_price_insecond" {
  description = "interval_of_fetching_market_price_insecond"
  type        = string
  default    = "60"
}
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




