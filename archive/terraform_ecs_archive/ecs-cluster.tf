data "aws_ecs_cluster" "main" {

  cluster_name = var.ecs_cluster_name
}