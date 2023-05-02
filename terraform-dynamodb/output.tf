# output configuration for lambda deployments 
#============
# Markets
# ===========
output "markets_table_name" {
  value = aws_dynamodb_table.markets.name
}

output "markets_gsi_info" {
  value = jsonencode(aws_dynamodb_table.markets.global_secondary_index)
}

#============
# Resources
# ===========
output "resources_table_name" {
  value = aws_dynamodb_table.resources.name
}

output "resources_gsi_info" {
  value = jsonencode(aws_dynamodb_table.resources.global_secondary_index)
}


#============
# Agents
# ===========
output "agents_table_name" {
  value = aws_dynamodb_table.agents.name
}

output "agents_gsi_info" {
  value = jsonencode(aws_dynamodb_table.agents.global_secondary_index)
}


#============
# Auctions
# ===========
output "auctions_table_name" {
  value = aws_dynamodb_table.auctions.name
}

output "auctions_gsi_info" {
  value = jsonencode(aws_dynamodb_table.auctions.global_secondary_index)
}
#============
# Devices
# ===========
output "devices_table_name" {
  value = aws_dynamodb_table.devices.name
}

output "devices_gsi_info" {
  value = jsonencode(aws_dynamodb_table.devices.global_secondary_index)
}

#============
# Orders
# ===========
output "orders_table_name" {
  value = aws_dynamodb_table.orders.name
}

output "orders_gsi_info" {
  value = jsonencode(aws_dynamodb_table.orders.global_secondary_index)
}


#============
# Dispatches
# ===========
output "dispatches_table_name" {
  value = aws_dynamodb_table.dispatches.name
}

output "dispatches_gsi_info" {
  value = jsonencode(aws_dynamodb_table.dispatches.global_secondary_index)
}

#============
# Meters
# ===========
output "meters_table_name" {
  value = aws_dynamodb_table.meters.name
}

output "meters_gsi_info" {
  value = jsonencode(aws_dynamodb_table.meters.global_secondary_index)
}


#============
# Settings
# ===========
output "settings_table_name" {
  value = aws_dynamodb_table.settings.name
}

output "settings_gsi_info" {
  value = jsonencode(aws_dynamodb_table.settings.global_secondary_index)
}

#============
# Readings
# ===========
output "readings_table_name" {
  value = aws_dynamodb_table.readings.name
}

output "readings_gsi_info" {
  value = jsonencode(aws_dynamodb_table.readings.global_secondary_index)
}

#============
# Settlements
# ===========
output "settlements_table_name" {
  value = aws_dynamodb_table.settlements.name
}

output "settlements_gsi_info" {
  value = jsonencode(aws_dynamodb_table.settlements.global_secondary_index)
}

#============
# Weather
# ===========
output "weather_table_name" {
  value = aws_dynamodb_table.weather.name
}

output "weather_gsi_info" {
  value = jsonencode(aws_dynamodb_table.weather.global_secondary_index)
}


#============
# S3 meta data
# ===========
output "shared_meta_data_s3_bucket" {
  value = aws_s3_bucket.meta_data_bucket.id
}


#============
# EVENT SQS
# ===========

output "devices_settings_event_sqs_id" {
    value = aws_sqs_queue.devices_settings_tables_event_sqs.id
}

# output "settings_table_event_sqs_id" {
#      value = aws_sqs_queue.settings_tables_event_sqs.id
# }