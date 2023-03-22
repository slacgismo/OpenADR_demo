### TEST ECS SERVICE
# variable "agent_definition_file"{
#   type = string
#   description = "The name of the file containing the agent task definition"
#   default = "./templates/ecs/container-definition-agent.json.tpl"
# }

# data "template_file" "agent_container_definitions" {
#   template = file(var.agent_definition_file)
#   vars = {
    
#     log_group_name   = aws_cloudwatch_log_group.agent_task_logs.name
#     log_group_region = var.aws_region
#   }
# }



# resource "aws_ecs_task_definition" "agent" {
#   family                   = "${var.prefix}-agnet-0"
# #   container_definitions    = data.template_file.agent_container_definitions.rendered
#   container_definitions    = data.template_file.agent_container_definitions.rendered
#   requires_compatibilities = ["FARGATE"]
#   network_mode             = "awsvpc"
#   cpu                      = 256
#   memory                   = 1024
#   execution_role_arn       = aws_iam_role.task_execution_role.arn
#   task_role_arn            = aws_iam_role.app_iam_role.arn
#   volume {
#     name = "agent-volume"
#   } 
#   tags = local.common_tags
# }





# resource "aws_ecs_service" "agnet" {
#   name             = "${var.prefix}-agent-0"
#   cluster          = aws_ecs_cluster.main.name
#   task_definition  = aws_ecs_task_definition.agent.family
#   desired_count    = 1
#   launch_type      = "FARGATE"
#   platform_version = "1.4.0"


#   network_configuration {
#     subnets = module.vpc.private_subnets
#     # security_groups = [module.private_openadr_sg.this_security_group_id]
#     security_groups  = [aws_security_group.ecs_agent_service.id]
#   }

# }




# resource "aws_ecs_service" "agent" {
#   name             = "${var.prefix}-agnet-0"
#   cluster          = aws_ecs_cluster.main.name
#   task_definition  = aws_ecs_task_definition.agent.arn
# #   task_definition  = aws_ecs_task_definition.agent.family
#   desired_count    = 1
#   launch_type      = "FARGATE"
#   platform_version = "1.4.0"
#   network_configuration {
#     # subnets = module.vpc.public_subnets
#     subnets          = module.vpc.public_subnets
#     security_groups  = [module.private_openadr_sg.this_security_group_id]
#     assign_public_ip = true
#   }
#   tags = local.common_tags
# }

# module "public_vtn_sg" {
#   source  = "terraform-aws-modules/security-group/aws"
#   version = "3.18.0"

#   name        = "public-bastion-sg"
#   description = "Security Group with SSH port open for everybody (IPv4 CIDR), egress ports are all world open"
#   vpc_id      = module.vpc.vpc_id
#   # Ingress Rules & CIDR Blocks
#   ingress_rules       = ["ssh-tcp", "http-8080-tcp"]
#   ingress_cidr_blocks = ["0.0.0.0/0"]
#   # Egress Rule - all-all open
#   egress_rules = ["all-all"]
#   tags         = local.common_tags
# }




variable "devices_worker_task_definition_file" {
  type        = string
  description = "The name of the file containing the devices worker task definition"
  default     = "devices_worker_task_definition.json.tpl"
}
variable "number_of_devices_worker" {
  type        = string
  description = "The name of the file containing the devices worker task definition"
  default     = 1
}


data "template_file" "devices_worker_container_definitions" {
  template = file("./templates/ecs/devices_worker_task_definition.json.tpl")
  vars = {
    devices_worker_name="${var.prefix}-devices-worker"
    FIFO_SQS_URL="${aws_sqs_queue.opneadr_workers_sqs.url}"
    BACKEND_S3_BUCKET_NAME="${aws_s3_bucket.agents.bucket}"
    AWS_REGION="${var.aws_region}"
    FIFO_DLQ_URL="${aws_sqs_queue.worker_dlq.url}"
    DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME="${aws_dynamodb_table.agenets_shared_state_lock.name}"
    HEALTH_CHEKC_PORT="${var.devices_worker_health_check_port}"
    log_group_name="${aws_cloudwatch_log_group.worker_task_logs.name}"
    log_group_region="${var.aws_region}"
  }
}

resource "aws_ecs_task_definition" "devices_worker" {
    
  family                   = "${var.prefix}-devices-worker"
  container_definitions    = data.template_file.devices_worker_container_definitions.rendered
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 1024
  execution_role_arn       = aws_iam_role.device_worker_execution_role.arn
  task_role_arn            = aws_iam_role.device_worker_iam_role.arn
  tags = local.common_tags
}

# # 
# TODO:deploy ecs-service 
# current issue:
# the ecs security group is not correct configured



# # create ecs service base on number of devices worker


# resource "aws_ecs_service" "devices_worker" {
#   for_each = { for i in range(var.number_of_devices_worker) : i => i }
 
#   name            = "${var.prefix}-devices-worker-7"
#   cluster          = aws_ecs_cluster.main.id
#   task_definition  = aws_ecs_task_definition.devices_worker.arn
# #   task_definition  = aws_ecs_task_definition.agent.family
#   desired_count    = 1
#   launch_type      = "FARGATE"
#   platform_version = "1.4.0"
#   network_configuration {
#     subnets          = module.vpc.private_subnets
#     security_groups  = [aws_security_group.devices_worker_sg.id]
#     assign_public_ip = false
#   }
#   tags = local.common_tags
# }

