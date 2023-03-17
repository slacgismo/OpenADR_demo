# # Create a Null Resource and Provisioners
# Create the terraform.auto.tfvars file of the devices_admin worker terraform_dyanmodb folder
# aws_region="xxxx"
# environment="xx"
# project="xxx"
# prefix="xxxxx"
# creator="xxxx"
# managedBy="xxxx"
#ECSBackendDynamoDBLockName="xxxx" dynamic setting

resource "null_resource" "exports_terrafrom_auto_tfvars_to_devices_admin_worker_terraform_dynamodb" {
  triggers = {
    aws_s3_bucket_name = aws_s3_bucket.agents.bucket

  }
  provisioner "local-exec" {
   command = <<-EOT
      echo 'project = "${var.project}"' >> terraform.auto.tfvars
      echo 'environment = "${var.environment}"' >> terraform.auto.tfvars
      echo 'aws_region = "${var.aws_region}"' >> terraform.auto.tfvars
      echo 'prefix = "${var.prefix}"' >> terraform.auto.tfvars
      echo 'creator = "${var.creator}"' >> terraform.auto.tfvars
      echo 'managedBy = "${var.managedBy}"' >> terraform.auto.tfvars
      echo '# dynamic setting ECSBackendDynamoDBLockName' >> terraform.auto.tfvars
    EOT
    # save to devices admin worker terraform folder
    working_dir = "${path.module}/services/devices_admin/worker/terraform_dynamodb"
    #on_failure = continue
  }
}

# aws_region="xxx"
# environment="xx"
# project="xx"
# prefix="xxx"
# creator="xx"
# managedBy="xxx"
# cloudwatch_name="xxxx"
# ecs_cluster_name="xxx"
# ecs_task_execution_role_name="xxxx"
# ecs_task_role_name="xxx"
# private_sg_name="pxxxx"
# private_vpc_id="xxx"
# task_definition_file="xxxx" dynamic setting
# agent_id="xxx" dynamic setting

resource "null_resource" "exports_terrafrom_auto_tfvars_to_devices_admin_worker_terraform_ecs" {
  triggers = {
    aws_s3_bucket_name = aws_s3_bucket.agents.bucket

  }
  provisioner "local-exec" {
   command = <<-EOT
      echo 'project = "${var.project}"' >> terraform.auto.tfvars
      echo 'environment = "${var.environment}"' >> terraform.auto.tfvars
      echo 'aws_region = "${var.aws_region}"' >> terraform.auto.tfvars
      echo 'prefix = "${var.prefix}"' >> terraform.auto.tfvars
      echo 'creator = "${var.creator}"' >> terraform.auto.tfvars
      echo 'managedBy = "${var.managedBy}"' >> terraform.auto.tfvars
      echo 'cloudwatch_name = "${aws_cloudwatch_log_group.agent_task_logs.name}"' >> terraform.auto.tfvars
      echo 'ecs_cluster_name = "${aws_ecs_cluster.main.name}"' >> terraform.auto.tfvars
      echo 'ecs_task_execution_role_name = "${aws_iam_role.task_execution_role.name}"' >> terraform.auto.tfvars
      echo 'ecs_task_role_name = "${aws_iam_role.app_iam_role.name}"' >> terraform.auto.tfvars
      echo 'private_sg_name = "${module.private_ven_sg.this_security_group_name}"' >> terraform.auto.tfvars
      echo 'private_vpc_id = "${module.vpc.vpc_id}"' >> terraform.auto.tfvars
      echo '# dynamic setting task_definition_file' >> terraform.auto.tfvars
      echo '# dynamic setting agent_id' >> terraform.auto.tfvars
    EOT
    # save to devices admin worker terraform folder
    working_dir = "${path.module}/services/devices_admin/worker/terraform_ecs"
    #on_failure = continue
  }
}

