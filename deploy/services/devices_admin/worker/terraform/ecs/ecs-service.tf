


data "template_file" "agent_container_definitions" {
  template = file("./templates/${var.task_definition_file}")
  vars = {
    environment   = var.environment
    SAVE_DATA_URL = var.SAVE_DATA_URL
    GET_VENS_URL = var.GET_VENS_URL
    PARTICIPATED_VENS_URL = var.PARTICIPATED_VENS_URL
    app_image_vtn = var.app_image_vtn
    app_image_ven = var.app_image_ven
    cloudwatch_name = data.aws_cloudwatch_log_group.openadr_logs.name
    aws_region = var.aws_region
    MOCK_DEVICES_API_URL = var.MOCK_DEVICES_API_URL
    vtn_address = var.vtn_address
    vtn_port = var.vtn_port
    MARKET_PRICES_URL = var.MARKET_PRICES_URL
  }
}



resource "aws_ecs_task_definition" "agent" {
  family                   = "${var.prefix}-${var.agent_id}"
#   container_definitions    = data.template_file.agent_container_definitions.rendered
  container_definitions    = data.template_file.agent_container_definitions.rendered
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 1024
  execution_role_arn       = data.aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = data.aws_iam_role.ecs_task_role.arn
  volume {
    name = "agent-volume"
  } 
  tags = local.common_tags
}



resource "aws_ecs_service" "agent" {
  name             = "${var.prefix}-${var.agent_id}"
  cluster          = data.aws_ecs_cluster.main.cluster_name
  task_definition  = aws_ecs_task_definition.agent.arn
#   task_definition  = aws_ecs_task_definition.agent.family
  desired_count    = 1
  launch_type      = "FARGATE"
  platform_version = "1.4.0"
  network_configuration {
    # subnets = module.vpc.public_subnets
    subnets          = data.aws_subnet_ids.private.ids
    security_groups  = [data.aws_security_group.private_sg.id]
    assign_public_ip = false
  }
  tags = local.common_tags
}



