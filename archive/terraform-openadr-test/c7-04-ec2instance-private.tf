# AWS EC2 Instance Terraform Module
# EC2 Instances that will be created in VPC Private Subnets
module "ec2_private" {
  depends_on = [module.vpc] # VERY VERY IMPORTANT else userdata webserver provisioning will fail
  source     = "terraform-aws-modules/ec2-instance/aws"
  version    = "2.17.0"
  # insert the 10 required variables here
  name          = "${var.prefix}-${var.environment}-vtn"
  ami           = data.aws_ami.amzlinux2.id
  instance_type = var.instance_type
  key_name      = var.instance_keypair
  #monitoring             = true
  vpc_security_group_ids = [module.private_sg.this_security_group_id]
  #subnet_id              = module.vpc.public_subnets[0]  
  subnet_ids = [
    module.vpc.private_subnets[0],
    module.vpc.private_subnets[1]
  ]
  instance_count = var.private_instance_count
  # user_data      = file("${path.module}/app1-install.sh")
  user_data = base64encode(
    templatefile(
      "./app1-install.sh", 
      {
        TIMEZONE          ="America/Los_Angeles"
        SAVE_DATA_URL          = "https://lv55k5wqj2.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
        GET_VENS_URL          = "https://lv55k5wqj2.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
      } 
    )
  )
  tags           = local.common_tags
}