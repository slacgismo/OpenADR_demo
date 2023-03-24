resource "aws_ecs_cluster" "main" {
  name = "${var.prefix}-${var.environment}-agents-cluster"

  tags = local.common_tags
}

