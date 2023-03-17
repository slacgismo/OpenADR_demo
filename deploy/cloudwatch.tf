resource "aws_cloudwatch_log_group" "agent_task_logs" {
  name = "${var.prefix}-ecs-agent"

  tags = local.common_tags
}

