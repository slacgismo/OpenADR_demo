resource "aws_cloudwatch_log_group" "agent_task_logs" {
  name = "${var.prefix}-ecs-agent"

  tags = local.common_tags
}

# resource "aws_cloudwatch_log_group" "ven_task_logs" {
#   name = "${var.prefix}-ecs-ven"

#   tags = local.common_tags
# }
