# # AWS EC2 Instance Terraform Module
# # Bastion Host - EC2 Instance that will be created in VPC Public Subnet

# locals {
#   csv_data = csvdecode(file("${path.module}/templates/batteries.csv"))
# }

# module "ec2_vtn_ven_csv" {
#   source  = "terraform-aws-modules/ec2-instance/aws"
#   count = length(local.csv_data)
#   # for_each = { for battery in local.csv_data : battery.battery_token => battery }
#   # battery_token = each.value.battery_token
#   # battery_sn =  each.value.battery_sn
#   version = "2.17.0"
#   depends_on = [module.ec2_vtn]
#   # insert the 10 required variables here
#   name = "${var.prefix}-${var.environment}-ven-${count.index}"
#   #instance_count         = 5
#   ami           = data.aws_ami.amzlinux2.id
#   instance_type = var.instance_type
#   key_name      = var.instance_keypair

#   #monitoring             = true
#   subnet_id              = module.vpc.public_subnets[0]
#   vpc_security_group_ids = [module.public_ven_sg.this_security_group_id]
#   iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
#   user_data = base64encode(
#     templatefile(
#       "./templates/ven-install.sh", 
#       {
#         TIMEZONE            ="America/Los_Angeles"
        
#         VTN_URL             = "http://${module.ec2_vtn.private_ip[0]}:8080/OpenADR2/Simple/2.0b"
#         VEN_NAME            = var.ven_name
#         BATTERY_TOKEN       = local.csv_data[count.index].battery_token
#         BATTERY_SN          = local.csv_data[count.index].battery_sn
#         DEVICE_ID           = var.device_id
#         DEVICE_TYPE         = var.device_type
#         PRICE_THRESHOLD     = var.price_threshold
#       } 
#     )
#   )
#   tags                   = local.common_tags
# }


