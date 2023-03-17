# # Create a Null Resource and Provisioners
# Create the backend.hcl file of the devices_admin worker terraform_dyanmodb folder
# bucket         = "xxxx"
# key            = "xxxxx"
# region         = "xxxx"
# encrypt        = true
# dynamodb_table = "xxxx"


resource "null_resource" "exports_s3_state_bucket_to_backend_hcl" {
  triggers = {
    aws_s3_bucket_name = aws_s3_bucket.agents.bucket

  }
  provisioner "local-exec" {
   command = <<-EOT
      echo 'bucket = "${aws_s3_bucket.agents.bucket}"' >> backend.hcl
      echo 'key = "${var.prefix}-${var.environment}-devices_admin.tfstate"' >> backend.hcl
      echo 'region = "${var.aws_region}"' >> backend.hcl
      echo 'encrypt = true' >> backend.hcl
    EOT
    # save to devices admin worker terraform folder
    working_dir = "${path.module}/services/devices_admin/worker/terraform_dynamodb"
    #on_failure = continue
  }
}


resource "null_resource" "exports_dynamodb_name_to_backend_hcl" {
  triggers = {
    dynamodb_agents_state_lock_table = aws_dynamodb_table.agenets_state_lock.name

  }
  provisioner "local-exec" {
   command = <<-EOT
      echo 'dynamodb_table = "${aws_dynamodb_table.agenets_state_lock.name}"' >> backend.hcl
    EOT
    working_dir = "${path.module}/services/devices_admin/worker/terraform_dynamodb"
    #on_failure = continue
  }
}

