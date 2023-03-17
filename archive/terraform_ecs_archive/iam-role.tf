data "aws_iam_role" "ecs_task_execution_role" {
  name = var.ecs_task_execution_role_name
}

data "aws_iam_role" "ecs_task_role" {
  name = var.ecs_task_role_name
}

