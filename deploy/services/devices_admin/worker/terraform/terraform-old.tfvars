# Create from main deployment
project = "TESS"
environment = "dev"
aws_region = "us-east-2"
prefix = "openadr"
creator = "Jimmy Leu"
managedBy = "Terraform"
cloudwatch_name = "openadr-ecs-agent"
ecs_cluster_name = "openadr-dev-agents-cluster"
ecs_task_execution_role_name = "openadr-task-exec-role"
ecs_task_role_name = "openadr-vtn-task"
private_sg_name = "public-bastion-sg-20230311232022989900000002"
private_vpc_id = "vpc-012a219f9778e1158"
# terraform_ecs_backend_bucket = "openadr-agents-state"
SAVE_DATA_URL = "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
GET_VENS_URL = "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
MARKET_PRICES_URL = "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/market_prices"
PARTICIPATED_VENS_URL = "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/participated_vens"
MOCK_DEVICES_API_URL = "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/battery_api"
vtn_address = "127.0.0.1"
vtn_port = "8080"
app_image_vtn = "041414866712.dkr.ecr.us-east-2.amazonaws.com/vtn:latest"
app_image_ven = "041414866712.dkr.ecr.us-east-2.amazonaws.com/ven:latest"
# dynamic setting agent_id
# dynamic setting task_definition_file
# agent_id="00ccff430c4bcfa1f1186f488b88fc"
# task_definition_file="task-definition-00ccff430c4bcfa1f1186f488b88fc.json.tpl"