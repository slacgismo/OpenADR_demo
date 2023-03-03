

# read ven_infos data from json file
locals {
  subscriptions =jsondecode(file("${path.module}/templates/ecs/ven_infos.json"))
}

data "template_file" "ven_container_definitions" {
  template = templatefile("${path.module}/templates/ecs/container-definitions-ven.json.tpl", {
    ven_infos = local.subscriptions,
    vtn_url = "http://${aws_lb.vtn.dns_name}:8080/OpenADR2/Simple/2.0b"
    ecr_image_ven = var.ecr_image_ven,
    mock_battery_api_url = var.mock_battery_api_url,
    ven_log_group_name = aws_cloudwatch_log_group.ven_task_logs.name
    log_group_region = var.aws_region
    dev = var.dev,
   })
}

# data "template_file" "ven_container_definitions" {

  
#   template = file("./templates/ecs/container-definitions-ven-clone.json.tpl")

#   vars = {
#     app_image        = var.ecr_image_ven
#     dev              = var.dev 
#     ven_id         = "ven0"
#     vtn_url          = "http://${aws_lb.vtn.dns_name}:8080/OpenADR2/Simple/2.0b"
#     mock_battery_api_url = var.mock_battery_api_url
#     battery_token    = "12321321qsd"
#     battery_sn       = "66354"
#     device_id        = "device_01"
#     device_type      = "SONNEN_BATTERY"
#     timezone         = var.timezone
#     price_threshold  = "0.15"
#     interval_of_fetching_device_data_insecond = "10"
#     report_duration_insecond = "3600"
#     report_specifier_id = "SONNEN_BATTERY"
#     log_group_name   = aws_cloudwatch_log_group.ven_task_logs.name
#     log_group_region = var.aws_region
#   }
# }


resource "aws_ecs_task_definition" "ven" {

  family                   = "${var.prefix}-ven"
  # container_definitions    = data.template_file.ven_container_definitions.rendered
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.task_execution_role.arn
  task_role_arn            = aws_iam_role.app_iam_role.arn
  # Define the volume and its source
  volume {
    name = "ven-volume"
  }
  container_definitions    = data.template_file.ven_container_definitions.rendered


  tags = local.common_tags
}



resource "aws_ecs_service" "ven" {
  name             = "${var.prefix}-ven"
  cluster          = aws_ecs_cluster.main.name
  task_definition  = aws_ecs_task_definition.ven.family
  desired_count    = 1
  launch_type      = "FARGATE"
  platform_version = "1.4.0"

  network_configuration {
    # subnets = module.vpc.public_subnets
    subnets = [
        module.vpc.private_subnets[0],
        module.vpc.private_subnets[1]
    ]
    security_groups  = [module.private_ven_sg.this_security_group_id]
    # assign_public_ip = true
  }


}


