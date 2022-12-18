data "aws_ami" "amazon_linux" {
  most_recent = true
  filter {
    name   = "name"
    values = ["amzn2-ami-kernel-5.10-hvm-2.0.*-x86_64-gp2"]
  }
  owners = ["amazon"]
}

resource "aws_instance" "ec2" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t2.micro"
  user_data     = file("./templates/ec2/user-data.sh")

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-ec2" })
  )
  subnet_id = aws_subnet.public_a.id
  vpc_security_group_ids = [
    aws_security_group.ec2.id
  ]


}


resource "aws_security_group" "ec2" {
  description = "Control bastion inbound and outbound access"
  name        = "${local.prefix}-ec2"
  vpc_id      = aws_vpc.main.id

  # Allow outbound port 22 and 8080
  ingress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
  # ingress {
  #   protocol    = "tcp"
  #   from_port   = 22
  #   to_port     = 22
  #   cidr_blocks = ["0.0.0.0/0"]
  # }

  # ingress {
  #   protocol    = "tcp"
  #   from_port   = 8080
  #   to_port     = 8080
  #   cidr_blocks = ["0.0.0.0/0"]
  # }

  # Allow outbound all traffic
  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.common_tags
}


