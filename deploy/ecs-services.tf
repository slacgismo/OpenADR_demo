### TEST ECS SERVICE
# variable "agent_definition_file"{
#   type = string
#   description = "The name of the file containing the agent task definition"
#   default = "./templates/ecs/agents/container-definition-agent.json.tpl"
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
#     security_groups  = [aws_security_group.ecs_agent_sg.id]
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


#================================================================================================
# # create devices worker task definition
#================================================================================================


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
  template = file("./templates/ecs/worker/devices_worker_task_definition.json.tpl")
  vars = {
    devices_worker_name="${var.prefix}-devices-worker"
    FIFO_SQS_URL="${aws_sqs_queue.opneadr_workers_sqs.url}"
    BACKEND_S3_BUCKET_NAME="${aws_s3_bucket.agents.bucket}"
    AWS_REGION="${var.aws_region}"
    FIFO_DLQ_URL="${aws_sqs_queue.worker_dlq.url}"
    DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME="${aws_dynamodb_table.agenets_shared_state_lock.name}"
    HEALTH_CHEKC_PORT="${var.devices_worker_health_check_port}"
    ECS_CLUSTER_NAME="${aws_ecs_cluster.main.name}"
    log_group_name="${aws_cloudwatch_log_group.worker_task_logs.name}"
    log_group_region="${var.aws_region}"
  }
}

resource "aws_ecs_task_definition" "devices_worker" {
    
  family                   = "${var.prefix}-devicesWorker"
  container_definitions    = data.template_file.devices_worker_container_definitions.rendered
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 1024
  execution_role_arn       = aws_iam_role.device_workers_execution_role.arn
  task_role_arn            = aws_iam_role.devices_workers_iam_role.arn
  tags = local.common_tags
}



# # create ecs service base on number of devices worker


resource "aws_ecs_service" "devices_worker" {
  # depends_on = [null_resource.build_and_push_docker_images_for_devices_admin_worker]
  for_each = { for i in range(var.number_of_devices_worker) : i => i }
 
  name            = "${var.prefix}-devicesWorker-12"
  cluster          = aws_ecs_cluster.main.id
  task_definition  = aws_ecs_task_definition.devices_worker.arn
#   task_definition  = aws_ecs_task_definition.agent.family
  desired_count    = 1
  launch_type      = "FARGATE"
  platform_version = "1.4.0"
  network_configuration {
    subnets          = module.vpc.private_subnets
    security_groups  = [aws_security_group.devices_worker_sg.id]
    assign_public_ip = false
  }
  tags = local.common_tags
}

