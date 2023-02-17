data "aws_ami" "amazon_linux" {
  most_recent = true
  filter {
    name   = "name"
    values = ["amzn2-ami-kernel-5.10-hvm-2.0.*-x86_64-gp2"]
  }
  owners = ["amazon"]
}

# data "template_file" "init" {
#   template = "${file("./templates/vtn/vtn-user-data.sh.tpl")}"
#   # depends = [
#   #   aws_db_instance.main.address,
#   #   aws_db_instance.main.db_name,
#   #   aws_db_instance.main.username,
#   #   aws_db_instance.main.password
#   # ]
#   vars = {
#     DB_HOST          = aws_db_instance.main.address
#     DB_NAME          = aws_db_instance.main.db_name
#     DB_USER          = aws_db_instance.main.username
#     DB_PASSWORD          = aws_db_instance.main.password
#   }
# }

# locals {
#   db_host       = aws_db_instance.main.address
#   db_name       = aws_db_instance.main.db_name
#   db_user      = aws_db_instance.main.username
#   db_pass  = aws_db_instance.main.password
# }
    

resource "aws_instance" "vtn" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t2.micro"
  # user_data     = file("./templates/vtn/vtn-user-data.sh")
  user_data = base64encode(
    templatefile(
      "./templates/vtn/vtn-user-data.sh", 
      {
        DB_HOST          = aws_db_instance.main.address
        DB_NAME          = aws_db_instance.main.db_name
        DB_USER          = aws_db_instance.main.username
        DB_PASSWORD          = aws_db_instance.main.password
        # db_address      = local.db_address
        # admin_user      = local.variable1
        # admin_password  = local.variable2
        # public_alb_dns  = local.private_alb_dns
      } 
    )
  )
  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-vtn" })
  )
  subnet_id = aws_subnet.public_a.id
  vpc_security_group_ids = [
    aws_security_group.vtn.id
  ]


}


resource "aws_security_group" "vtn" {
  description = "Control vtn inbound and outbound access"
  name        = "${local.prefix}-vtn"
  vpc_id      = aws_vpc.main.id

  # Allow outbound port 22 and 8080
  # ingress {
  #   protocol    = "-1"
  #   from_port   = 0
  #   to_port     = 0
  #   cidr_blocks = ["0.0.0.0/0"]
  # }
  # Ingress
  ingress {
    protocol    = "tcp"
    from_port   = 22
    to_port     = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol    = "tcp"
    from_port   = 8080
    to_port     = 8080
    cidr_blocks = ["0.0.0.0/0"]
  }
  # Egress
  // HTTPS
  egress {
    protocol    = "tcp"
    from_port   = 8080
    to_port     = 8080
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = ["0.0.0.0/0"]
  }
  // HTTP
  egress {
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }
  // database
  egress {
    from_port = 5432
    to_port   = 5432
    protocol  = "tcp"
    cidr_blocks = [
      aws_subnet.private_a.cidr_block,
      # aws_subnet.private_b.cidr_block,
    ]
  }
  # Allow outbound all traffic
  # egress {
  #   protocol    = "-1"
  #   from_port   = 0
  #   to_port     = 0
  #   cidr_blocks = ["0.0.0.0/0"]
  # }

  tags = local.common_tags
}


