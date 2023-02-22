# AWS EC2 Instance Terraform Module
# Bastion Host - EC2 Instance that will be created in VPC Public Subnet

module "ec2_public" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "2.17.0"
  # insert the 10 required variables here
  name = "${var.prefix}-${var.environment}-vtn"
  #instance_count         = 5
  ami           = data.aws_ami.amzlinux2.id
  instance_type = var.instance_type
  key_name      = var.instance_keypair
  
  #monitoring             = true
  subnet_id              = module.vpc.public_subnets[0]
  vpc_security_group_ids = [module.public_bastion_sg.this_security_group_id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
  user_data = base64encode(
    templatefile(
      "./templates/vtn-install.sh", 
      {
        TIMEZONE          ="America/Los_Angeles"
        SAVE_DATA_URL          = "https://lv55k5wqj2.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
        GET_VENS_URL          = "https://lv55k5wqj2.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
      } 
    )
  )
  tags                   = local.common_tags
}

