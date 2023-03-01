
# # read battery data from csv file
# # read battery data from csv file
# locals {
#   batteries_data = csvdecode(file("${path.module}/templates/batteries.csv"))
# }




# resource "aws_ecs_task_definition" "ven" {
#   count = length(local.batteries_data)
#   family                   = "${var.prefix}-ven-${count.index}"
#   # container_definitions    = data.template_file.ven_container_definitions.rendered
#   requires_compatibilities = ["FARGATE"]
#   network_mode             = "awsvpc"
#   cpu                      = 256
#   memory                   = 512
#   execution_role_arn       = aws_iam_role.task_execution_role.arn
#   task_role_arn            = aws_iam_role.app_iam_role.arn
#   volume {
#     name = "static"
#   }
#   container_definitions    = jsonencode(
#     [
#       {
#           "name": "ven",
#           "image": "${app_image}",
#           "essential": true,
#           "memoryReservation": 256,
#           "environment": [
#               DEV  = "True",
#               BATTERY_SN            = list.get(local.batteries_data[count.index], index(local.headers, "battery_sn")),
#               BATTERY_TOKEN      = list.get(local.batteries_data[count.index], index(local.headers, "battery_token")),
#               VEN_NAME = = list.get(local.batteries_data[count.index], index(local.headers, "ven_name")),
#               DEVICE_ID = list.get(local.batteries_data[count.index], index(local.headers, "device_id")),
#               PRICE_THRESHOLD = list.get(local.batteries_data[count.index], index(local.headers, "price_threshold")),
#               VTN_URL = "http://${aws_lb.vtn.dns_name}:8080/OpenADR2/Simple/2.0b",
#               MOCK_BATTERY_API_URL = "${var.mock_battery_api_url}",
#               DEVICE_TYPE = "${var.device_type}",
#               TIMEZONE = "${var.timezone}"
#           ],
#           "runtimePlatform": {
#               "operatingSystemFamily": "LINUX",
#               "cpuArchitecture": "ARM64"
#           },
#           "entryPoint": [ "sh", "-c" ],
#           "command": [ "python ven.py" ],
#           "logConfiguration": {
#               "logDriver": "awslogs",
#               "options": {
#                   "awslogs-group": "${log_group_name}",
#                   "awslogs-region": "${log_group_region}",
#                   "awslogs-stream-prefix": "ven"
#               }
#           }
#       }
#     ]


#   )

#   tags = local.common_tags
# }



# resource "aws_ecs_service" "ven" {
#   count = length(local.batteries_data)
#   name             = "${var.prefix}-ven"
#   cluster          = aws_ecs_cluster.main.name
#   task_definition  = aws_ecs_task_definition.ven.*.arn[count.index]
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
