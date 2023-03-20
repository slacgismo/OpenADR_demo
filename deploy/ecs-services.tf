
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
    worker_fifo_sqs_url="${aws_sqs_queue.opneadr_workers_sqs.url}"
    backend_s3_bucket_devices_admin="${aws_s3_bucket.agents.bucket}"
    aws_region="${var.aws_region}"
    worker_dlq_url="${aws_sqs_queue.worker_dlq.url}"
    ecs_cluster_name="${aws_ecs_cluster.main.name}"
    dynamodb_agents_shared_remote_state_lock_table_name="${aws_dynamodb_table.agenets_shared_state_lock.name}"
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
  execution_role_arn       = aws_iam_role.task_execution_role.arn
  task_role_arn            = aws_iam_role.app_iam_role.arn
  volume {
    name = "devices-worker-volume"
  } 
  tags = local.common_tags
}

# 
# TODO:deploy ecs-service 
# current issue:
# the ecs security group is not correct configured



# create ecs service base on number of devices worker


# resource "aws_ecs_service" "devices_worker" {
#   for_each = { for i in range(var.number_of_devices_worker) : i => i }
 
#   name            = "${var.prefix}-devices-worker-${each.value}"
#   cluster          = aws_ecs_cluster.main.id
#   task_definition  = aws_ecs_task_definition.devices_worker.arn
# #   task_definition  = aws_ecs_task_definition.agent.family
#   desired_count    = 1
#   launch_type      = "FARGATE"
#   platform_version = "1.4.0"
#   network_configuration {
#     # subnets = module.vpc.public_subnets
#     subnets          = module.vpc.private_subnets
#     security_groups  = [module.private_openadr_sg.this_security_group_id]
#     assign_public_ip = false
#   }
#   tags = local.common_tags
# }

