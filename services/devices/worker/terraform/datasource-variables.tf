
# Cloudwatch 
variable "cloudwatch_name"{
    description =""
    type = string

}

# ECS cluster
variable "ecs_cluster_name"{
    description =""
    type = string

}


# IAM Role and task execution role
variable "ecs_task_execution_role_name"{
    description =""
    type = string

}

variable "ecs_task_role_name"{
    description =""
    type = string

}
# Security Group
variable "ecs_agent_sg"  {
  description = "ecs agent security group"
  type        = string
}



# VPC 
variable "private_vpc_id" {
    description =""
    type = string

}


