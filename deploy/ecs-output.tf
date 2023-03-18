# ecs_vtn public ip
# output "ecs_public_ip" {
#   description = "List of public IP addresses assigned to the instances"
#   value       = aws_ecs_service.vtn.*.network_configuration.0.assign_public_ip
# }

output "cluster_arn" {
  value = aws_ecs_cluster.main.arn
}

output "app_iam_role_arn" {
  value = aws_iam_role.app_iam_role.arn
}

output "task_execution_role" {
  value = aws_iam_role.task_execution_role.arn
}