# # AWS EC2 Instance Terraform Module
# # Bastion Host - EC2 Instance that will be created in VPC Public Subnet

# # read battery data from csv file
# locals {
#   batteries_data = csvdecode(file("${path.module}/templates/batteries.csv"))
# }


# module "ec2_ven" {
  
#   source  = "terraform-aws-modules/ec2-instance/aws"
#   version = "2.17.0"
#   depends_on = [aws_lb.vtn]

#   # number of vens
#   count = length(local.batteries_data)

#   name = "${var.prefix}-${var.environment}-private-${local.batteries_data[count.index].ven_id}"
#   #instance_count         = 5
#   ami           = data.aws_ami.amzlinux2.id
#   instance_type = var.instance_type
#   key_name      = var.instance_keypair
#   # iam_instance_profile = aws_iam_instance_profile.ven.name
#   monitoring             = true 
#   # subnet_id              = module.vpc.public_subnets[0]
#   subnet_id              = module.vpc.private_subnets[0]
#   vpc_security_group_ids = [module.private_ven_sg.this_security_group_id]
#   iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name

#   user_data = base64encode(
#     templatefile(
#       "./templates/ven-install.sh", 
#       {
#         DEV                 = var.dev
#         TIMEZONE            = var.timezone
#         VEN_NAME            = local.batteries_data[count.index].ven_name
#         VTN_URL             = "http://${aws_lb.vtn.dns_name}:8080/OpenADR2/Simple/2.0b"
#         MOCK_BATTERY_API_URL = var.mock_battery_api_url
#         BATTERY_TOKEN       = local.batteries_data[count.index].battery_token
#         BATTERY_SN          = local.batteries_data[count.index].battery_sn
#         DEVICE_ID           = local.batteries_data[count.index].device_id
#         DEVICE_TYPE         = var.device_type
#         PRICE_THRESHOLD     = local.batteries_data[count.index].price_threshold
#       } 
#     )
#   )
  
#   tags                   = local.common_tags
# }


