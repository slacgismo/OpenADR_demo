

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
    devices_worker_name                                 = "${var.prefix}-devices-worker"
    FIFO_SQS_URL                                        = "${data.aws_sqs_queue.opneadr_workers_sqs.url}"
    BACKEND_S3_BUCKET_NAME                              = "${aws_s3_bucket.device_shared.bucket}"
    AWS_REGION                                          = "${var.aws_region}"
    DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME = "${aws_dynamodb_table.agenets_shared_state_lock.name}"
    HEALTH_CHEKC_PORT                                   = "${var.devices_worker_health_check_port}"
    ECS_CLUSTER_NAME                                    = "${aws_ecs_cluster.main.name}"
    log_group_name                                      = "${aws_cloudwatch_log_group.worker_task_logs.name}"
    log_group_region                                    = "${var.aws_region}"
    WORKER_PORT                                         = "${var.worker_port}"
    ENVIRONMENT                                                 = "${var.environment}"

  }
}

resource "aws_ecs_task_definition" "devices_worker" {

  family                   = "${var.prefix}-${var.client}-${var.environment}-devices-worker"
  container_definitions    = data.template_file.devices_worker_container_definitions.rendered
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 1024
  execution_role_arn       = aws_iam_role.device_workers_execution_role.arn
  task_role_arn            = aws_iam_role.devices_workers_iam_role.arn
  tags                     = local.common_tags
}



# # create ecs service base on number of devices worker


# resource "aws_ecs_service" "devices_worker" {
#   # depends_on = [null_resource.build_and_push_docker_images_for_devices_admin_worker]
#   for_each = { for i in range(var.number_of_devices_worker) : i => i }

#   name            = "${var.prefix}-devicesWorker-12"
#   cluster         = aws_ecs_cluster.main.id
#   task_definition = aws_ecs_task_definition.devices_worker.arn
#   #   task_definition  = aws_ecs_task_definition.agent.family
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

