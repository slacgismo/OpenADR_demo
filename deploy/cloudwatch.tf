resource "aws_cloudwatch_log_group" "agent_task_logs" {
  name = "${var.prefix}-ecs-agent"

  tags              = local.common_tags
  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "worker_task_logs" {
  name = "${var.prefix}-devices-worker"

  tags              = local.common_tags
  retention_in_days = 30
}

