


data "template_file" "vtn_container_definitions" {
  template = file("templates/ecs/container-definitions-vtn.json.tpl")

  vars = {
    app_image        = var.ecr_image_vtn
    timezone         = var.timezone
    save_data_url    = var.save_data_url
    vtn_id          = var.vtn_id
    get_vens_url     = var.get_vens_url
    market_prices_url = var.market_prices_url
    participated_vens_url = var.participated_vens_url
    interval_of_fetching_market_price_insecond = var.interval_of_fetching_market_price_insecond
    log_group_name   = aws_cloudwatch_log_group.ecs_task_logs.name
    log_group_region = var.aws_region
  }
}

resource "aws_ecs_task_definition" "vtn" {
  family                   = "${var.prefix}-vtn"
  container_definitions    = data.template_file.vtn_container_definitions.rendered
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.task_execution_role.arn
  task_role_arn            = aws_iam_role.app_iam_role.arn
  volume {
    name = "vtn-volume"
  } 

  tags = local.common_tags
}



resource "aws_ecs_service" "vtn" {
  name             = "${var.prefix}-vtn"
  cluster          = aws_ecs_cluster.main.name
  task_definition  = aws_ecs_task_definition.vtn.family
  desired_count    = 1
  launch_type      = "FARGATE"
  platform_version = "1.4.0"


#   subnet_id              = module.vpc.public_subnets[0]


  network_configuration {
    # subnets = module.vpc.public_subnets
    subnets = [
        module.vpc.private_subnets[0],
        module.vpc.private_subnets[1]
    ]
    security_groups  = [module.public_vtn_sg.this_security_group_id]
    # assign_public_ip = true
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.vtn.arn
    container_name   = "vtn"
    container_port   = 8080
  }

}
