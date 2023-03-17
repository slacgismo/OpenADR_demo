# # Create a Null Resource and Provisioners
# # Create a Null Resource and Provisioners
# Create the backend.hcl file of the devices_admin worker terraform_dyanmodb folder
# bucket         = "xxxx"
# key            = "xxxxx"
# region         = "xxxx"
# encrypt        = true
# dynamodb_table = "xxxx"


# resource "null_resource" "exports_s3_state_bucket_to_backend_hcl" {
#   depends_on=[aws_dynamodb_table.terraform_state_lock_table]

#   provisioner "local-exec" {
#    command = <<-EOT
#       echo 'bucket = "${var.backend_s3_bucket_devices_admin}"' > backend.hcl
#       echo 'key = "${var.prefix}-${var.environment}-devices_admin.tfstate"' >> backend.hcl
#       echo 'region = "${var.aws_region}"' >> backend.hcl
#       echo 'dynamodb_table = "${var.backend_dyanmodb_table_teraform_state_lock_devices_admin}"' >> backend.hcl
#       echo 'encrypt = true' >> backend.hcl
#     EOT
#     # save to devices admin worker terraform folder
#     working_dir = "${path.module}/ecs"
#     #on_failure = continue
#   }
# }





