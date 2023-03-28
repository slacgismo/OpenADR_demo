# The below AWS resouces was created by Terraform main deployment 
# In the production, those resources are created by Github Actions
# The variables are pass from Github Actions to Terraform as enviroment variables

# Cloudwatch 
data "aws_cloudwatch_log_group" "openadr_logs" {
  name = var.cloudwatch_name
}

# ECS cluster
data "aws_ecs_cluster" "main" {

  cluster_name = var.ecs_cluster_name
}

# IAM Role and task execution role
data "aws_iam_role" "ecs_task_execution_role" {
  name = var.ecs_task_execution_role_name
}

data "aws_iam_role" "ecs_task_role" {
  name = var.ecs_task_role_name
}

# Security Group
data "aws_security_group" "ecs_agent_sg" {
  name = var.ecs_agent_sg
}


data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [var.private_vpc_id]
  }
}