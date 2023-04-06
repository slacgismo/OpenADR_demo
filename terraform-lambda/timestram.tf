
resource "aws_timestreamwrite_database" "measurements" {
  database_name = "${var.prefix}-${var.client}-${var.environment}-measurements-timestream-db"
  tags          = local.common_tags
}