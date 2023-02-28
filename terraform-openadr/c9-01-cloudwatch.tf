resource "aws_cloudwatch_log_group" "ecs_task_logs" {
  name = "${var.prefix}-ecs-vtn"

  tags = local.common_tags
}
