resource "aws_ecr_repository" "openadr_generator" {
  name         = "openadr-generator"
  tags         = local.common_tags
  force_delete = true
}



resource "aws_ecr_repository" "vtn" {
  name         = "vtn"
  tags         = local.common_tags
  force_delete = true
}


resource "aws_ecr_repository" "ven" {
  name         = "ven"
  tags         = local.common_tags
  force_delete = true
}
