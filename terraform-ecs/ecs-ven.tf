
data "template_file" "ven_container_definitions" {
  template = file("templates/ecs/container-definitions-ven.json.tpl")

  vars = {
    app_image        = var.ecr_image_ven
    ven_name         = "ven123"
    vtn_url          = "http://3.17.184.76:8080/OpenADR2/Simple/2.0b"
    battery_token    = var.battery_token
    battery_sn       = var.battery_sn
    device_id        = var.device_id
    device_type      = var.device_type
    timezone         = var.timezone
    price_threshold  = var.price_threshold
    log_group_name   = aws_cloudwatch_log_group.ecs_task_logs.name
    log_group_region = data.aws_region.current.name
  }
}


resource "aws_ecs_task_definition" "ven" {
  family                   = "${local.prefix}-ven"
  container_definitions    = data.template_file.ven_container_definitions.rendered
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.task_execution_role.arn
  task_role_arn            = aws_iam_role.app_iam_role.arn
  volume {
    name = "static"
  }

  tags = local.common_tags
}


resource "aws_security_group" "ecs_ven_service" {
  description = "Access for the ECS service"
  name        = "${local.prefix}-ecs-ven-service"
  vpc_id      = aws_vpc.main.id

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

  egress {
    from_port = 5432
    to_port   = 5432
    protocol  = "tcp"
    cidr_blocks = [
      aws_subnet.private_a.cidr_block,
      aws_subnet.private_b.cidr_block,
    ]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }


  tags = local.common_tags
}

resource "aws_ecs_service" "ven" {
  name             = "${local.prefix}-ven"
  cluster          = aws_ecs_cluster.main.name
  task_definition  = aws_ecs_task_definition.ven.family
  desired_count    = 1
  launch_type      = "FARGATE"
  platform_version = "1.4.0"

  network_configuration {
    subnets = [
      aws_subnet.public_a.id,
      aws_subnet.public_b.id,
    ]
    security_groups  = [aws_security_group.ecs_ven_service.id]
    assign_public_ip = true
  }
}
