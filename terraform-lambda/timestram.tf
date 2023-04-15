
resource "aws_timestreamwrite_database" "measurements" {
  database_name = "${var.prefix}-${var.client}-${var.environment}-measurements-timestream-db"
  tags          = local.common_tags
}

resource "aws_timestreamwrite_table" "readings" {
  database_name = aws_timestreamwrite_database.measurements.name
  table_name    =   = "${var.prefix}-${var.client}-${var.environment}-readings"
  retention_properties {
    memory_store_retention_period_in_hours = 24
    magnetic_store_retention_period_in_days = 30
  }
  tags = local.common_tags
}