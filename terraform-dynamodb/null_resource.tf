# Create a Null Resource and Provisioners

resource "null_resource" "export_terrafrom_tfvars_to_output" {
  depends_on = [
    aws_s3_bucket.meta_data_bucket,
    aws_dynamodb_table.devices,
    aws_dynamodb_table.settings,
    aws_dynamodb_table.orders,
    aws_dynamodb_table.dispatches,
    aws_dynamodb_table.meters,
    aws_dynamodb_table.agents,
    aws_dynamodb_table.readings,
    aws_dynamodb_table.resources,
    aws_dynamodb_table.markets,
    aws_dynamodb_table.weather,
    aws_dynamodb_table.settlements,
    aws_dynamodb_table.auctions,
    aws_sqs_queue.devices_tables_event_sqs,
    aws_sqs_queue.settings_tables_event_sqs
  ]
  # always run this resource
  triggers = {
    always_run = timestamp()
  }
  provisioner "local-exec" {
    command = <<-EOT
        echo '# Create from dynamodb deployment' > terraform.tfvars
        echo '# Dynamodb settings' >> terraform.tfvars
        echo 'devices_table_name="${aws_dynamodb_table.devices.name}"' >> terraform.tfvars
        echo 'settings_table_name="${aws_dynamodb_table.settings.name}"' >> terraform.tfvars
        echo 'orders_table_name="${aws_dynamodb_table.orders.name}"' >> terraform.tfvars
        echo 'dispatches_table_name="${aws_dynamodb_table.dispatches.name}"' >> terraform.tfvars
        echo 'meters_table_name="${aws_dynamodb_table.meters.name}"' >> terraform.tfvars
        echo 'agents_table_name="${aws_dynamodb_table.agents.name}"' >> terraform.tfvars
        echo 'readings_table_name="${aws_dynamodb_table.readings.name}"' >> terraform.tfvars
        echo 'resources_table_name="${aws_dynamodb_table.resources.name}"' >> terraform.tfvars
        echo 'markets_table_name="${aws_dynamodb_table.markets.name}"' >> terraform.tfvars
        echo 'weather_table_name="${aws_dynamodb_table.weather.name}"' >> terraform.tfvars
        echo 'settlements_table_name="${aws_dynamodb_table.settlements.name}"' >> terraform.tfvars
        echo 'auctions_table_name="${aws_dynamodb_table.auctions.name}"' >> terraform.tfvars
        echo '# GSI settings' >> terraform.tfvars
        
        echo  'resources_gsi_info="${replace(jsonencode(aws_dynamodb_table.resources.global_secondary_index), "\"", "\\\"")}"' >> terraform.tfvars
        echo  'settlements_gsi_info="${replace(jsonencode(aws_dynamodb_table.settlements.global_secondary_index), "\"", "\\\"")}"' >> terraform.tfvars
        echo  'auctions_gsi_info="${replace(jsonencode(aws_dynamodb_table.auctions.global_secondary_index), "\"", "\\\"")}"' >> terraform.tfvars
        echo  'weather_gsi_info="${replace(jsonencode(aws_dynamodb_table.weather.global_secondary_index), "\"", "\\\"")}"' >> terraform.tfvars
        echo  'markets_gsi_info="${replace(jsonencode(aws_dynamodb_table.markets.global_secondary_index), "\"", "\\\"")}"' >> terraform.tfvars
        echo  'readings_gsi_info="${replace(jsonencode(aws_dynamodb_table.readings.global_secondary_index), "\"", "\\\"")}"' >> terraform.tfvars
        echo  'agents_gsi_info="${replace(jsonencode(aws_dynamodb_table.agents.global_secondary_index), "\"", "\\\"")}"' >> terraform.tfvars
        echo  'meters_gsi_info="${replace(jsonencode(aws_dynamodb_table.meters.global_secondary_index), "\"", "\\\"")}"' >> terraform.tfvars
        echo  'dispatches_gsi_info="${replace(jsonencode(aws_dynamodb_table.dispatches.global_secondary_index), "\"", "\\\"")}"' >> terraform.tfvars
        echo  'orders_gsi_info="${replace(jsonencode(aws_dynamodb_table.orders.global_secondary_index), "\"", "\\\"")}"' >> terraform.tfvars
        echo  'settings_gsi_info="${replace(jsonencode(aws_dynamodb_table.settings.global_secondary_index), "\"", "\\\"")}"' >> terraform.tfvars
        echo  'devices_gsi_info="${replace(jsonencode(aws_dynamodb_table.devices.global_secondary_index), "\"", "\\\"")}"' >> terraform.tfvars


        echo '# SQS settings' >> terraform.tfvars
        echo 'settings_tables_event_sqs_name="${aws_sqs_queue.settings_tables_event_sqs.name}"' >> terraform.tfvars
        echo 'devices_tables_event_sqs_name="${aws_sqs_queue.devices_tables_event_sqs.name}"' >> terraform.tfvars
        echo '# S3 settings' >> terraform.tfvars
        echo 'meta_data_bucket_name="${aws_s3_bucket.meta_data_bucket.id}"' >> terraform.tfvars
        echo '# S3 settings' >> terraform.tfvars
      echo '# dynamic setting task_definition_file' >> terraform.tfvars
    EOT
    # save to devices admin worker terraform folder
    working_dir = "./output"
  }
}







