# # Create a Null Resource and Provisioners

# resource "null_resource" "generate_ecs_task_definition_agents" {
# #   triggers = {
# #     python_file = md5(file("${path.module}/lambdas/git_client/index.py"))
# #     docker_file = md5(file("${path.module}/lambdas/git_client/Dockerfile"))
# #   }

#   provisioner "local-exec" {
#     command = <<EOF
#            #!/bin/bash
#            aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com
#            cd ${path.module}/lambdas/git_client
#            docker build -t ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag} .
#            docker push ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag}
#        EOF
#   }
# }
# resource "null_resource" "name" {
#   depends_on = [module.ec2_public]
#   # Connection Block for Provisioners to connect to EC2 Instance
#   connection {
#     type     = "ssh"
#     # host     = aws_eip.bastion_eip.public_ip    
#     host      = module.ec2_public.public_ip[0]
#     user     = "ec2-user"
#     password = ""
#     private_key = file("private-key/${var.instance_keypair}.pem")
#   }  

# ## File Provisioner: Copies the terraform-key.pem file to /tmp/terraform-key.pem
#   provisioner "file" {
#     source      = "private-key/${var.instance_keypair}.pem"
#     destination = "/tmp/${var.instance_keypair}.pem"
#   }
# ## Remote Exec Provisioner: Using remote-exec provisioner fix the private key permissions on Bastion Host
#   provisioner "remote-exec" {
#     inline = [
#       "sudo chmod 400 /tmp/${var.instance_keypair}.pem"
#     ]
#   }
# ## Local Exec Provisioner:  local-exec provisioner (Creation-Time Provisioner - Triggered during Create Resource)
#   provisioner "local-exec" {
#     command = "echo VPC created on `date` and VPC ID: ${module.vpc.vpc_id} >> creation-time-vpc-id.txt"
#     working_dir = "local-exec-output-files/"
#     #on_failure = continue
#   }
# ## Local Exec Provisioner:  local-exec provisioner (Destroy-Time Provisioner - Triggered during deletion of Resource)
# /*  provisioner "local-exec" {
#     command = "echo Destroy time prov `date` >> destroy-time-prov.txt"
#     working_dir = "local-exec-output-files/"
#     when = destroy
#     #on_failure = continue
#   }  
#   */

# }

# Creation Time Provisioners - By default they are created during resource creations (terraform apply)
# Destory Time Provisioners - Will be executed during "terraform destroy" command (when = destroy)