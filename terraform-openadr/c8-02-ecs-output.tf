## ecs_vtn public ip
# output "ecs_vtn_public_ip" {
#   description = "List of public IP addresses assigned to the instances"
#   value       = aws_ecs_service.vtn.*.network_configuration.0.assign_public_ip
# }