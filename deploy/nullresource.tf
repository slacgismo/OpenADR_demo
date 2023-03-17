# # Create a Null Resource and Provisioners
# # Create a Null Resource and Provisioners
# Create the backend.hcl file of the devices_admin worker terraform_dyanmodb folder
# bucket         = "xxxx"
# key            = "xxxxx"
# region         = "xxxx"
# encrypt        = true
# dynamodb_table = "xxxx"


resource "null_resource" "exports_s3_state_bucket_to_backend_hcl" {
  depends_on=[aws_s3_bucket.agents,aws_dynamodb_table.agenets_state_lock]

  provisioner "local-exec" {
   command = <<-EOT
      echo 'bucket = "${aws_s3_bucket.agents.bucket}"' > backend.hcl
      echo 'key = "${var.prefix}-${var.environment}-devices_admin.tfstate"' >> backend.hcl
      echo 'region = "${var.aws_region}"' >> backend.hcl
      echo 'encrypt = true' >> backend.hcl
      echo 'dynamodb_table = "${aws_dynamodb_table.agenets_state_lock.name}"' >> backend.hcl
    EOT
    # save to devices admin worker terraform folder
    working_dir = "${path.module}/services/devices_admin/worker/terraform"
    #on_failure = continue
  }
}



# Create the terraform.auto.tfvars file of the devices_admin worker terraform_dyanmodb folder
# aws_region="xxxx"
# environment="xx"
# project="xxx"
# prefix="xxxxx"
# creator="xxxx"
# managedBy="xxxx"
#ECSBackendDynamoDBLockName="xxxx" dynamic setting

resource "null_resource" "exports_terrafrom_tfvars_to_devices_admin_worker_terraform" {
   depends_on=[aws_s3_bucket.agents]

  provisioner "local-exec" {
   command = <<-EOT
      echo 'project="${var.project}"' > terraform.tfvars
      echo 'environment="${var.environment}"' >> terraform.tfvars
      echo 'aws_region="${var.aws_region}"' >> terraform.tfvars
      echo 'prefix="${var.prefix}"' >> terraform.tfvars
      echo 'creator="${var.creator}"' >> terraform.tfvars
      echo 'managedBy="${var.managedBy}"' >> terraform.tfvars
      echo 'backend_s3_bucket_devices_admin="${aws_s3_bucket.agents.bucket}"' >> terraform.tfvars
      
    EOT
    # save to devices admin worker terraform folder
    working_dir = "${path.module}/services/devices_admin/worker/terraform"
    #on_failure = continue
  }
}


resource "null_resource" "exports_terrafrom_tfvars_to_devices_admin_worker_terraform_ecs" {
  depends_on =[
    aws_s3_bucket.agents,
    aws_dynamodb_table.agenets_state_lock,
    aws_cloudwatch_log_group.agent_task_logs,
    aws_ecs_cluster.main,
    aws_iam_role.task_execution_role,
    aws_iam_role.app_iam_role,
    module.private_ven_sg,
    module.vpc.vpc_id,
    null_resource.exports_terrafrom_tfvars_to_devices_admin_worker_terraform
  ]

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
      echo 'private_sg_name="${module.private_ven_sg.this_security_group_name}"' >> terraform.tfvars
      echo 'private_vpc_id="${module.vpc.vpc_id}"' >> terraform.tfvars
      echo 'SAVE_DATA_URL="${var.save_data_url}"' >> terraform.tfvars
      echo 'GET_VENS_URL="${var.get_vens_url}"' >> terraform.tfvars
      echo 'MARKET_PRICES_URL="${var.market_prices_url}"' >> terraform.tfvars
      echo 'PARTICIPATED_VENS_URL="${var.participated_vens_url}"' >> terraform.tfvars
      echo 'MOCK_DEVICES_API_URL="${var.mock_devices_api_url}"' >> terraform.tfvars
      echo 'vtn_address="${var.vtn_address}"' >> terraform.tfvars
      echo 'vtn_port="${var.vtn_port}"' >> terraform.tfvars
      echo 'app_image_vtn="${var.app_image_vtn}"' >> terraform.tfvars
      echo 'app_image_ven="${var.app_image_ven}"' >> terraform.tfvars
      echo '# dynamic setting agent_id' >> terraform.tfvars
      echo '# dynamic setting task_definition_file' >> terraform.tfvars
    EOT
    # save to devices admin worker terraform folder
    working_dir = "${path.module}/services/devices_admin/worker/terraform/ecs"
    #on_failure = continue
  }
}

# create .env file for devices_admin worker folder
resource "null_resource" "create_env_file_for_devices_admin_worker" {
  depends_on =  [aws_sqs_queue.opneadr_workers_sqs]
    

  provisioner "local-exec" {
   command = <<-EOT
      echo 'worker_fifo_sqs_url="${aws_sqs_queue.opneadr_workers_sqs.url}"' > .env
      echo 'backend_s3_bucket_devices_admin="${aws_s3_bucket.agents.bucket}"' >> .env
    EOT
    # save to devices admin worker terraform folder
    working_dir = "${path.module}/services/devices_admin/worker"
    #on_failure = continue
  }
}