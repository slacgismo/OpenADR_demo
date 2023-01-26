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
