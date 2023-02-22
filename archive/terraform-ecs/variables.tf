variable "prefix" {
  default = "openadr"
}


variable "project" {
  default = "TESS"
}

variable "contact" {
  default = "Jimmy Leu"
}


variable "db_username" {
  description = "Username for the RDS Postgres instance"
}

variable "db_password" {
  description = "Password for the RDS postgres instance"
}

# variable "bastion_key_name" {
#   default = "JL_Beam"
# }

variable "ecr_image_vtn" {
  description = "ECR Image for VTN"
  default     = "041414866712.dkr.ecr.us-east-2.amazonaws.com/vtn:latest"
}

variable "ecr_image_ven" {
  description = "ECR Image for VEN"
  default     = "041414866712.dkr.ecr.us-east-2.amazonaws.com/ven:latest"
}

variable "timezone" {
  description = "Timezone of VTN"
  default     = "America/Los_Angeles"
}



# VTN vairbales
variable "save_data_url" {
  description = "Token of battery"
  default     = "https://lv55k5wqj2.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
  # a secret token 
}

variable "get_vens_url" {
  description = "Token of battery"
  default     = "https://lv55k5wqj2.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
  # a secret token 
}


# VEN variables
variable "battery_token" {
  description = "Token of battery"
  # a secret token 
}

variable "battery_sn" {
  description = "Battery SN"
  # a secret sn 
}
variable "device_id" {
  description = "device id"
  default     = "device_01"
  # a secret sn 
}
variable "device_type" {
  description = "device type"
  default     = "SONNEN_BATTERY"
  # a secret sn 
}
variable "price_threshold" {
  description = "price threshold"
  default     = "0.15"
  # a secret sn 
}

variable "ven_name" {
  description = "VEN name"
  default     = "ven123"
  # a secret sn 
}
