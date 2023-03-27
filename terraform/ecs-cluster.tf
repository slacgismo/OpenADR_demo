resource "aws_ecs_cluster" "main" {
  name = "${var.prefix}-${var.client}-${var.environment}-agent-cluster"

  tags = local.common_tags
}

