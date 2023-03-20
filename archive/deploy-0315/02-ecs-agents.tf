
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

  }

}



