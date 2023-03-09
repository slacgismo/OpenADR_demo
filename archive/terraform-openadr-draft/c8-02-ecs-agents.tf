
# locals {
#   agent_container_definitions = [
#     "${file("templates/ecs/container-definition-agent0.json.tpl")}",
#     "${file("templates/ecs/container-definition-agent1.json.tpl")}",
#   ]
# }

locals {
  agent_container_definitions = jsondecode(file(var.agent_definition_list_file))
}


data "template_file" "agent_container_definitions" {
  count    = length(local.agent_container_definitions)
#   template = element(local.agent_container_definitions, count.index)
#   template = file("templates/ecs/container-definition-agent0.json.tpl")
  template = file("./templates/ecs/${local.agent_container_definitions[count.index].definition_file_name}")
  vars = {
    log_group_name   = aws_cloudwatch_log_group.agent_task_logs.name
    log_group_region = var.aws_region
  }
}


# data "template_file" "agent_container_definitions" {
#   template = file("templates/ecs/container-definitions-agent.json.tpl")

#   vars = {
#     app_image_vtn        = var.ecr_image_vtn
#     save_data_url    = var.save_data_url
#     vtn_id          = var.vtn_id
#     get_vens_url     = var.get_vens_url
#     market_prices_url = var.market_prices_url
#     participated_vens_url = var.participated_vens_url
#     interval_of_fetching_market_price_insecond = var.interval_of_fetching_market_price_insecond
#     log_group_name   = aws_cloudwatch_log_group.agent_task_logs.name
#     log_group_region = var.aws_region
#     app_image_ven        = var.ecr_image_ven
#     env              = var.env 
#     ven_id          = "ven0"
#     vtn_url          = "http://127.0.0.1:8080/OpenADR2/Simple/2.0b"
#     mock_battery_api_url = var.mock_battery_api_url
#     battery_token    = "12321321qsd"
#     battery_sn       = "66354"
#     device_id        = "device_01"
#     device_type      = "SONNEN_BATTERY"
#     price_threshold  = "0.15"
#     interval_of_fetching_device_data_insecond = "10"
#     report_specifier_id = "SONNEN_BATTERY"
#   }
# }

resource "aws_ecs_task_definition" "agent" {
  count                    = length(local.agent_container_definitions)
  family                   = "${var.prefix}-agent-${count.index}"
#   container_definitions    = data.template_file.agent_container_definitions.rendered
  container_definitions    = data.template_file.agent_container_definitions[count.index].rendered
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 1024
  execution_role_arn       = aws_iam_role.task_execution_role.arn
  task_role_arn            = aws_iam_role.app_iam_role.arn
  volume {
    name = "agent-volume"
  } 
  tags = local.common_tags
}



resource "aws_ecs_service" "agent" {
  count            = length(local.agent_container_definitions)
  name             = "${var.prefix}-agent-${local.agent_container_definitions[count.index].agent_id}"
  cluster          = aws_ecs_cluster.main.name
  task_definition  = aws_ecs_task_definition.agent[count.index].arn
#   task_definition  = aws_ecs_task_definition.agent.family
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
#   load_balancer {
#     target_group_arn = aws_lb_target_group.agent.arn
#     container_name   = "vtn"
#     container_port   = 8080
#   }

}



