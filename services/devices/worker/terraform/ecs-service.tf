


data "template_file" "agent_container_definitions" {
  template = file("./templates/${var.task_definition_file}")
  vars = {
    environment   = var.environment
    METER_API_URL = var.METER_API_URL
    DEVICE_API_URL = var.DEVICE_API_URL
    DISPATCH_API_URL = var.DISPATCH_API_URL
    app_image_vtn = var.app_image_vtn
    app_image_ven = var.app_image_ven
    cloudwatch_name = data.aws_cloudwatch_log_group.openadr_logs.name
    aws_region = var.aws_region
    EMULATED_DEVICE_API_URL = var.EMULATED_DEVICE_API_URL
    vtn_address = var.vtn_address
    vtn_port = var.vtn_port
    ORDER_PAI_URL = var.ORDER_PAI_URL
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
  name             = "${var.prefix}-agent-${var.agent_id}"
  cluster          = data.aws_ecs_cluster.main.cluster_name
  task_definition  = aws_ecs_task_definition.agent.arn
#   task_definition  = aws_ecs_task_definition.agent.family
  desired_count    = 1
  launch_type      = "FARGATE"
  platform_version = "1.4.0"
  network_configuration {
    # subnets = module.vpc.public_subnets
    subnets          = data.aws_subnets.private.ids
    security_groups  = [data.aws_security_group.ecs_agent_sg.id]
    assign_public_ip = false
  }
  tags = local.common_tags
}



