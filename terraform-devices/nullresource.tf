# # Create a Null Resource and Provisioners

resource "null_resource" "export_terrafrom_tfvars_to_devices_admin_worker_terraform" {
  depends_on = [
    aws_s3_bucket.device_shared,
    aws_dynamodb_table.agenets_shared_state_lock,
    aws_cloudwatch_log_group.agent_task_logs,
    aws_ecs_cluster.main,
    aws_iam_role.task_execution_role,
    aws_iam_role.app_iam_role,
    aws_security_group.ecs_agent_sg,
    module.vpc.vpc_id,
  ]
  # always run this resource
  triggers = {
    always_run = timestamp()
  }
  provisioner "local-exec" {
    command = <<-EOT
      echo '# Create from main deployment' > terraform.tfvars
      echo 'project="${var.project}"' >> terraform.tfvars
      echo 'environment="${var.environment}"' >> terraform.tfvars
      echo 'aws_region="${var.aws_region}"' >> terraform.tfvars
      echo 'prefix="${var.prefix}"' >> terraform.tfvars
      echo 'creator="${var.creator}"' >> terraform.tfvars
      echo 'managedBy="${var.managedBy}"' >> terraform.tfvars
      echo 'cloudwatch_name="${aws_cloudwatch_log_group.agent_task_logs.name}"' >> terraform.tfvars
      echo 'ecs_cluster_name="${aws_ecs_cluster.main.name}"' >> terraform.tfvars
      echo 'ecs_task_execution_role_name="${aws_iam_role.task_execution_role.name}"' >> terraform.tfvars
      echo 'ecs_task_role_name="${aws_iam_role.app_iam_role.name}"' >> terraform.tfvars
      echo 'ecs_agent_sg="${aws_security_group.ecs_agent_sg.name}"' >> terraform.tfvars
      echo 'private_vpc_id="${module.vpc.vpc_id}"' >> terraform.tfvars
      echo 'meters_api_url="${var.meters_api_url}"' >> terraform.tfvars
      echo 'devices_api_url="${var.device_api_url}"' >> terraform.tfvars
      echo 'orders_api_url="${var.order_api_url}"' >> terraform.tfvars
      echo 'dispatches_api_url="${var.dispatch_api_url}"' >> terraform.tfvars
      echo 'emulated_device_api_url="${var.emulated_device_api_url}"' >> terraform.tfvars
      echo 'vtn_address="${var.vtn_address}"' >> terraform.tfvars
      echo 'vtn_port="${var.vtn_port}"' >> terraform.tfvars
      echo 'app_image_vtn="${var.app_image_vtn}"' >> terraform.tfvars
      echo 'app_image_ven="${var.app_image_ven}"' >> terraform.tfvars
      echo '# dynamic setting agent_id' >> terraform.tfvars
      echo '# dynamic setting task_definition_file' >> terraform.tfvars
    EOT
    # save to devices admin worker terraform folder
    working_dir = "../services/devices/worker/terraform"
  }
}

# create .env file for devices_admin worker folder
resource "null_resource" "export_env_file_for_devices_admin_worker" {
  depends_on = [data.aws_sqs_queue.opneadr_workers_sqs]

  # always run this resource
  triggers = {
    always_run = timestamp()
  }
  provisioner "local-exec" {
    command = <<-EOT
      echo 'FIFO_SQS_URL="${data.aws_sqs_queue.opneadr_workers_sqs.url}"' > .env
      echo 'BACKEND_S3_BUCKET_NAME="${aws_s3_bucket.device_shared.bucket}"' >> .env
      echo 'AWS_REGION="${var.aws_region}"' >> .env
      echo 'HEALTH_CHEKC_PORT="${var.devices_worker_health_check_port}"' >> .env
      echo 'DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME="${aws_dynamodb_table.agenets_shared_state_lock.name}"' >> .env
      echo 'ECS_CLUSTER_NAME="${aws_ecs_cluster.main.name}"' >> .env
      echo 'ENV="${var.environment}"'>> .env
      echo 'WORKER_PORT="${var.worker_port}"'>> .env
    EOT
    # save to devices admin worker terraform folder
    working_dir = "../services/devices/worker"
  }
}

# create .env file for devices_admin worker folder
# resource "null_resource" "exports_env_file_for_devices_admin_cli" {
#   depends_on = [data.aws_sqs_queue.opneadr_workers_sqs]

#   # always run this resource

#   triggers = {
#     always_run = timestamp()
#   }
#   provisioner "local-exec" {
#     command = <<-EOT
#       echo 'FIFO_SQS_URL="${data.aws_sqs_queue.opneadr_workers_sqs.url}"' > .env
#       echo 'ECS_CLUSTER_NAME="${aws_ecs_cluster.main.name}"'>> .env
#       echo 'ENV="${var.environment}"'>> .env
#       echo 'BACKEND_S3_BUCKET_NAME="${aws_s3_bucket.device_shared.bucket}"' >> .env
#     EOT
#     # save to devices admin cli folder
#     working_dir = "../services/devices/cli"

#   }
# }


#================================================================================================
# build and push docker images for device admin worker, ven and vtn
#================================================================================================

# resource "null_resource" "build_and_push_docker_images_for_devices_admin_worker" {
#   depends_on =[
#     aws_ecr_repository.devices_worker
#   ]

#   provisioner "local-exec" {
#     command = <<EOF
#            #!/bin/bash
#            aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com
#            docker-compose -f ./services/devices/docker-compose.yml build
#            docker tag -t devices_worker ${aws_ecr_repository.devices_worker.repository_url}:latest .
#            docker push ${aws_ecr_repository.devices_worker.repository_url}:latest
#        EOF
#   }
# }


# resource "null_resource" "build_and_push_docker_images_for_vtn_and_ven" {
#   depends_on =[
#     aws_ecr_repository.ven,
#     aws_ecr_repository.vtn
#   ]

#   provisioner "local-exec" {
#     command = <<EOF
#            #!/bin/bash
#            aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com
#            docker-compose -f ./services/docker-compose.yml build .
#            docker tag -t services_ven ${aws_ecr_repository.ven.repository_url}:latest .
#            docker tag -t services_vtn ${aws_ecr_repository.vtn.repository_url}:latest .
#            docker push ${aws_ecr_repository.vtn.repository_url}:latest
#            docker push ${aws_ecr_repository.ven.repository_url}:latest
#        EOF
#   }
# }
