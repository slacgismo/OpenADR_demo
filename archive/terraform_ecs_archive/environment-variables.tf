variable "ecs_cluster_name" {
  description = "The name of the ECS cluster that create by main terraform deployment"
  # default     = "openadr-dev-agents-cluster"
}


variable "public_sg_name" {
  description = "Name of the private security group from main deployment"
  # default = "public-bastion-sg-20230309182512418300000004"
}


data "external" "ecs_task_execution_role_name" {
  description = "Name of ecs_task_execution_role from main deployment"
  # default = "openadr-task-exec-role"
}

variable  "ecs_task_role_name" {
  description = "Name of ecs_task_role from main deployment"
  # default = "openadr-task-exec-role"
}

variable "private_vpc_id" {
  description = "private vpc id from main deployment"
  # default = "vpc-0bb7cf40077966b7f"
}


variable  "cloudwatch_name" {
  description = "The name of the cloudwatch log group"
  # default = "openadr-ecs-agent"

}

variable "agent_id"{
  description = "The id of the agent"
  # default = "agent0"
}