# AWS EC2 Instance Terraform Variables
# EC2 Instance Variables

# AWS EC2 Instance Type
variable "instance_type" {
  description = "EC2 Instance Type"
  type        = string
  default     = "t2.micro"
}

# AWS EC2 Instance Key Pair
variable "instance_keypair" {
  description = "AWS EC2 Key pair that need to be associated with EC2 Instance"
  type        = string
  default     = "JL-Beam"
}

# AWS EC2 Private Instance Count
variable "private_instance_count" {
  description = "AWS EC2 Private Instances Count"
  type        = number
  default     = 1
}

variable "ven_name" {
  description = "VEN Name"
  default = "ven123"
}
variable "battery_token" {
  description = "Battery token"
}
variable "battery_sn" {
  description = "Battery sn"
}
variable "device_id" {
  description = "Device ID"
  default = "device_01"
}
variable "device_type" {
  description = "Device type"
  default = "SONNEN_BATTERY"
}
variable "price_threshold" {
  description = "Price threshold "
  default = "0.15"
}

