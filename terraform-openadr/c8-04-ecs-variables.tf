# ECS  Variables


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




