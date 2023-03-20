resource "aws_ecr_repository" "devices_worker" {
  name                 = "devices_worker"
  tags = local.common_tags
}

resource "aws_ecr_repository" "device_cli" {
  name                 = "device_cli"
  tags = local.common_tags
}


resource "aws_ecr_repository" "vtn" {
  name                 = "vtn"
  tags = local.common_tags
}


resource "aws_ecr_repository" "ven" {
  name                 = "ven"
  tags = local.common_tags
}
