variable "prefix" {
  default = "openadr"
}


variable "project" {
  default = "tess"
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
  default     = "041414866712.dkr.ecr.us-east-2.amazonaws.com/openleadr-vtn:latest"
}

