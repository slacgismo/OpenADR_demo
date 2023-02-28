resource "aws_lb" "vtn" {
  name               = "${var.prefix}-vtn-alb"
  load_balancer_type = "application"
  subnets = [
    module.vpc.public_subnets[0],
    module.vpc.public_subnets[1]
  ]
  # security_groups = [aws_security_group.lb.id]
  security_groups = [module.loadbalancer_sg.this_security_group_id]
  tags = local.common_tags
}

resource "aws_lb_target_group" "vtn" {
  name        = "${var.prefix}-vtn"
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "ip"
  port        = 8080

  health_check {
    path = "/vens"
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

