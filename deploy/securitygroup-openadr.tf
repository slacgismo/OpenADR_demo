


resource "aws_security_group" "devices_worker_sg" {
  description = "Access for the ECS service"
  name        = "${var.prefix}-ecs-devices-worker-sg"
  vpc_id      = module.vpc.vpc_id

  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 8070
    to_port     = 8070
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8070
    to_port     = 8070
    protocol    = "tcp"
    # this should be the [module.vpc.vpc_cidr_block]
    # TODO: change this to the vpc cidr block,
    # If we chnage this to the vpc cidr block, we will not be able to access the ECR service to download the docker images
    cidr_blocks = ["0.0.0.0/0"]


  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    # this should be the [module.vpc.vpc_cidr_block]
    # TODO: change this to the vpc cidr block,
    # If we chnage this to the vpc cidr block, we will not be able to access the ECR service to download the docker images
    cidr_blocks = ["0.0.0.0/0"]
  }


  tags = local.common_tags
}

resource "aws_security_group" "ecs_agent_sg" {
  description = "Access for the ECS service"
  name        = "${var.prefix}-ecs-agent-sg"
  vpc_id      = module.vpc.vpc_id

  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    # this should be the [module.vpc.vpc_cidr_block]
    # TODO: change this to the vpc cidr block,
    # If we chnage this to the vpc cidr block, we will not be able to access the ECR service to download the docker images
    cidr_blocks = ["0.0.0.0/0"]


  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    # this should be the [module.vpc.vpc_cidr_block]
    # TODO: change this to the vpc cidr block,
    # If we chnage this to the vpc cidr block, we will not be able to access the ECR service to download the docker images
    cidr_blocks = ["0.0.0.0/0"]
  }


  tags = local.common_tags
}



# module "private_openadr_sg" {
#   source  = "terraform-aws-modules/security-group/aws"
#   version = "3.18.0"

#   name        = "private-openadr-sg"
#   description = "Security Group with SSH port open for everybody (IPv4 CIDR), egress ports are all world open"
#   vpc_id      = module.vpc.vpc_id
#   # Ingress Rules & CIDR Blocks
#   ingress_rules       = ["ssh-tcp", "http-8080-tcp","http-80-tcp"]
#   # ingress_cidr_blocks = ["0.0.0.0/0"]
#   ingress_cidr_blocks = [module.vpc.vpc_cidr_block]
#   # Egress Rule - all-all open
#   egress_rules = ["http-8080-tcp"]
#   # egress_cidr_blocks = ["0.0.0.0/0"]
#   egress_cidr_blocks = [module.vpc.vpc_cidr_block]
#   tags         = local.common_tags
# }



# module "private_devices_worker_sg" {
#   source  = "terraform-aws-modules/security-group/aws"
#   version = "3.18.0"

#   name        = "private-openadr-sg"
#   description = "Security Group with SSH port open for everybody (IPv4 CIDR), egress ports are all world open"
#   vpc_id      = module.vpc.vpc_id
#   # Ingress Rules & CIDR Blocks
#   ingress_rules       = ["ssh-tcp", "http-8070-tcp"]
#   ingress_cidr_blocks = [module.vpc.vpc_cidr_block]
#   # Egress Rule - all-all open
#   egress_rules = ["http-8070-tcp"]
#   egress_cidr_blocks = [module.vpc.vpc_cidr_block]
#   tags         = local.common_tags
# }

