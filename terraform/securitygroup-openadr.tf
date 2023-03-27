


resource "aws_security_group" "devices_worker_sg" {
  description = "Access for the ECS service"
  name        = "${var.prefix}-${var.client}-${var.environment}-ecs-devices-worker-sg"
  vpc_id      = module.vpc.vpc_id



  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }


  ingress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"
    # this should be the [module.vpc.vpc_cidr_block]
    # TODO: change this to the vpc cidr block,
    # If we chnage this to the vpc cidr block, we will not be able to access the ECR service to download the docker images
    cidr_blocks = ["0.0.0.0/0"]
  }


  tags = local.common_tags
}

resource "aws_security_group" "ecs_agent_sg" {
  description = "Access for the ECS service"
  name        = "${var.prefix}-${var.client}-${var.environment}-ecs-agent-sg"

  vpc_id = module.vpc.vpc_id


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
    # cidr_blocks = [module.vpc.vpc_cidr_block]
  }

  ingress {
    from_port = 8080
    to_port   = 8080
    protocol  = "tcp"
    # this should be the [module.vpc.vpc_cidr_block]
    # TODO: change this to the vpc cidr block,
    # If we chnage this to the vpc cidr block, we will not be able to access the ECR service to download the docker images
    cidr_blocks = ["0.0.0.0/0"]
    # cidr_blocks = [module.vpc.vpc_cidr_block]


  }

  ingress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"
    # this should be the [module.vpc.vpc_cidr_block]
    # TODO: change this to the vpc cidr block,
    # If we chnage this to the vpc cidr block, we will not be able to access the ECR service to download the docker images
    cidr_blocks = ["0.0.0.0/0"]
  }


  tags = local.common_tags
}




