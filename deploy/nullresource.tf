# # Create a Null Resource and Provisioners

resource "null_resource" "exports_terrafrom_tfvars_to_devices_admin_worker_terraform" {
  depends_on =[
    aws_s3_bucket.agents,
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
      echo 'METER_API_URL="${var.meter_api_url}"' >> terraform.tfvars
      echo 'DEVICE_API_URL="${var.device_api_url}"' >> terraform.tfvars
      echo 'ORDER_PAI_URL="${var.order_api_url}"' >> terraform.tfvars
      echo 'DISPATCH_API_URL="${var.dispatch_api_url}"' >> terraform.tfvars
      echo 'EMULATED_DEVICE_API_URL="${var.emulated_device_api_url}"' >> terraform.tfvars
      echo 'vtn_address="${var.vtn_address}"' >> terraform.tfvars
      echo 'vtn_port="${var.vtn_port}"' >> terraform.tfvars
      echo 'app_image_vtn="${var.app_image_vtn}"' >> terraform.tfvars
      echo 'app_image_ven="${var.app_image_ven}"' >> terraform.tfvars
      echo '# dynamic setting agent_id' >> terraform.tfvars
      echo '# dynamic setting task_definition_file' >> terraform.tfvars
    EOT
    # save to devices admin worker terraform folder
    working_dir = "${path.module}/services/devices/worker/terraform"
  }
}

# create .env file for devices_admin worker folder
resource "null_resource" "exports_env_file_for_devices_admin_worker" {
  depends_on =  [aws_sqs_queue.opneadr_workers_sqs]
    
  # always run this resource
  triggers = {
    always_run = timestamp()
  }
  provisioner "local-exec" {
   command = <<-EOT
      echo 'FIFO_SQS_URL="${aws_sqs_queue.opneadr_workers_sqs.url}"' > .env
      echo 'BACKEND_S3_BUCKET_NAME="${aws_s3_bucket.agents.bucket}"' >> .env
      echo 'AWS_REGION="${var.aws_region}"' >> .env
      echo 'FIFO_DLQ_URL="${aws_sqs_queue.worker_dlq.url}"' >> .env
      echo 'HEALTH_CHEKC_PORT="${var.devices_worker_health_check_port}"' >> .env
      echo 'DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME="${aws_dynamodb_table.agenets_shared_state_lock.name}"' >> .env
      echo 'ECS_CLUSTER_NAME="${aws_ecs_cluster.main.name}"' >> .env
    EOT
    # save to devices admin worker terraform folder
    working_dir = "${path.module}/services/devices/worker"
  }
}

# create .env file for devices_admin worker folder
resource "null_resource" "exports_env_file_for_devices_admin_cli" {
  depends_on =  [aws_sqs_queue.opneadr_workers_sqs]
    
  # always run this resource
  triggers = {
    always_run = timestamp()
  }
  provisioner "local-exec" {
   command = <<-EOT
      echo 'worker_fifo_sqs_url="${aws_sqs_queue.opneadr_workers_sqs.url}"' > .env
      echo 'ecs_cluster_name=${aws_ecs_cluster.main.name}"'>> .env

    EOT
    # save to devices admin worker terraform folder
    working_dir = "${path.module}/services/devices/cli"

  }
}


