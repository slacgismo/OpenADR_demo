data "aws_subnet_ids" "private" {
  vpc_id            = var.private_vpc_id
  # filter {
  #   name   = "tag:Name"
  #   values = ["TESS-dev-myvpc*"]
  # }
}

