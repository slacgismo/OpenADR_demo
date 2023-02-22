# AWS EC2 Instance Terraform Module
# Bastion Host - EC2 Instance that will be created in VPC Public Subnet

module "ec2_public_ven" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "2.17.0"
  depends_on = [module.ec2_public]
  # insert the 10 required variables here
  name = "${var.prefix}-${var.environment}-ven"
  #instance_count         = 5
  ami           = data.aws_ami.amzlinux2.id
  instance_type = var.instance_type
  key_name      = var.instance_keypair
  
  #monitoring             = true
  subnet_id              = module.vpc.public_subnets[0]
  vpc_security_group_ids = [module.public_ven_sg.this_security_group_id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
  user_data = base64encode(
    templatefile(
      "./templates/ven-install.sh", 
      {
        TIMEZONE            ="America/Los_Angeles"
        
        VTN_URL             = "http://${module.ec2_public.private_ip[0]}:8080/OpenADR2/Simple/2.0b"
        VEN_NAME            = var.ven_name
        BATTERY_TOKEN       = var.battery_token
        BATTERY_SN          = var.battery_sn
        DEVICE_ID           = var.device_id
        DEVICE_TYPE         = var.device_type
        PRICE_THRESHOLD     = var.price_threshold
      } 
    )
  )
  tags                   = local.common_tags
}


