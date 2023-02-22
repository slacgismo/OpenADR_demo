resource "aws_lb" "vtn" {
  name               = "${local.prefix}-main"
  load_balancer_type = "application"
  subnets = [
    aws_subnet.public_a.id,
    aws_subnet.public_b.id
  ]

  security_groups = [aws_security_group.lb.id]

  tags = local.common_tags
}

resource "aws_lb_target_group" "vtn" {
  name        = "${local.prefix}-vtn"
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"
  port        = 8080

  health_check {
    path = "/admin/login/"
  }
}

resource "aws_lb_listener" "vtn" {
  load_balancer_arn = aws_lb.vtn.arn
  port              = 8080
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.vtn.arn
  }
}

resource "aws_security_group" "lb" {
  description = "Allow access to Application Load Balancer"
  name        = "${local.prefix}-lb"
  vpc_id      = aws_vpc.main.id

  ingress {
    protocol    = "tcp"
    from_port   = 8080
    to_port     = 8080
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "tcp"
    from_port   = 8080
    to_port     = 8080
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.common_tags
}
