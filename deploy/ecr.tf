resource "aws_ecr_repository" "devices_admin" {
  name                 = "devices_admin"
  tags = local.common_tags
}


# resource "aws_ecr_repository" "vtn" {
#   name                 = "vtn"
#   tags = local.common_tags
# }


# resource "aws_ecr_repository" "ven" {
#   name                 = "ven"
#   tags = local.common_tags
# }
