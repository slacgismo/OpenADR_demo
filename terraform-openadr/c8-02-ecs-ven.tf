

# # read battery data from csv file
locals {
  batteries_data = csvdecode(file("${path.module}/templates/batteries.csv"))
}




resource "aws_ecs_task_definition" "ven" {
  count = length(local.batteries_data)
  family                   = "${var.prefix}-ven-${count.index}"
  # container_definitions    = data.template_file.ven_container_definitions.rendered
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.task_execution_role.arn
  task_role_arn            = aws_iam_role.app_iam_role.arn
  volume {
    name = "static"
  }
  container_definitions    = jsonencode(
    [
      {
          "name": "ven",
          "image": "${var.ecr_image_ven}",
          "essential": true,
          "memoryReservation": 256,
          "environment": [
            # battery_sn variable from  locals.batteries_data
            { "name": "BATTERY_SN", "value": "${local.batteries_data[count.index].battery_sn}" },
            { "name": "DEVICE_ID", "value": "${local.batteries_data[count.index].device_id}" },
            { "name": "DEVICE_TYPE", "value": "${var.device_type}" },
            { "name": "VEN_NAME", "value": "${local.batteries_data[count.index].ven_name}" },
            { "name": "VTN_URL", "value": "http://${aws_lb.vtn.dns_name}:8080/OpenADR2/Simple/2.0b" },
            { "name": "MOCK_BATTERY_API_URL", "value": "${var.mock_battery_api_url}" },
            { "name": "BATTERY_TOKEN", "value": "${local.batteries_data[count.index].battery_token}" },
            { "name": "TIMEZONE", "value": "${var.timezone}" },
            { "name": "PRICE_THRESHOLD", "value": "${local.batteries_data[count.index].price_threshold}" },
            { "name": "DEV", "value": "True" }
          ],
          "runtimePlatform": {
              "operatingSystemFamily": "LINUX",
              "cpuArchitecture": "ARM64"
          },
          "entryPoint": [ "sh", "-c" ],
          "command": [ "python ven.py" ],
          "logConfiguration": {
              "logDriver": "awslogs",
              "options": {
                  "awslogs-group": "${aws_cloudwatch_log_group.ecs_task_logs.name}",
                  "awslogs-region": "${var.aws_region}",
                  "awslogs-stream-prefix": "ven"
              }
          }
      }
    ]


  )

  tags = local.common_tags
}



resource "aws_ecs_service" "ven" {
  count = length(local.batteries_data)
  name             = "${var.prefix}-ven"
  cluster          = aws_ecs_cluster.main.name
  task_definition  = aws_ecs_task_definition.ven.*.arn[count.index]
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
    security_groups  = [module.private_ven_sg.this_security_group_id]
    # assign_public_ip = true
  }


}


# archive , define one ecs ven task


# read battery data from csv file

# data "template_file" "ven_container_definitions" {

  
#   template = file("templates/ecs/container-definitions-ven.json.tpl")

#   vars = {
#     app_image        = var.ecr_image_ven
#     dev              = var.dev 
#     ven_name         = "ven123"
#     vtn_url          = "http://${aws_lb.vtn.dns_name}:8080/OpenADR2/Simple/2.0b"
#     mock_battery_api_url = var.mock_battery_api_url
#     battery_token    = "12321321qsd"
#     battery_sn       = "66354"
#     device_id        = "device_01"
#     device_type      = "SONNEN_BATTERY"
#     timezone         = var.timezone
#     price_threshold  = "0.15"
#     log_group_name   = aws_cloudwatch_log_group.ven_task_logs.name
#     log_group_region = var.aws_region
#   }
# }



# resource "aws_ecs_task_definition" "ven" {
#   family                   = "${var.prefix}-ven"
#   container_definitions    = data.template_file.ven_container_definitions.rendered
#   requires_compatibilities = ["FARGATE"]
#   network_mode             = "awsvpc"
#   cpu                      = 256
#   memory                   = 512
#   execution_role_arn       = aws_iam_role.task_execution_role.arn
#   task_role_arn            = aws_iam_role.app_iam_role.arn
#   volume {
#     name = "static"
#   }

#   tags = local.common_tags
# }



# resource "aws_ecs_service" "ven" {
#   name             = "${var.prefix}-ven"
#   cluster          = aws_ecs_cluster.main.name
#   task_definition  = aws_ecs_task_definition.ven.family
#   desired_count    = 1
#   launch_type      = "FARGATE"
#   platform_version = "1.4.0"


# #   subnet_id              = module.vpc.public_subnets[0]


#   network_configuration {
#     # subnets = module.vpc.public_subnets
#     subnets = [
#         module.vpc.private_subnets[0],
#         module.vpc.private_subnets[1]
#     ]
#     security_groups  = [module.private_ven_sg.this_security_group_id]
#     # assign_public_ip = true
#   }


# }
