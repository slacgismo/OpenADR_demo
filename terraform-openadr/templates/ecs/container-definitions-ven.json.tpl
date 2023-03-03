${jsonencode([
    for ven_info in ven_infos :{
        "name" =  ven_info.ven_id,
        "image" =  ecr_image_ven,
        "essential": true,
        "memoryReservation": 256,
        "environment": [
            {"name" = "ENV", "value" = env},
            {"name" = "VEN_ID", "value" = ven_info.ven_id},
            {"name" =  "VTN_URL", "value" = vtn_url},
            {"name" = "MOCK_BATTERY_API_URL", "value" = mock_battery_api_url},
            {"name" = "BATTERY_TOKEN", "value" = ven_info.battery_token},
            {"name" =  "BATTERY_SN", "value" = ven_info.battery_sn},
            {"name" = "DEVICE_ID", "value" = ven_info.device_id},
            {"name" = "DEVICE_TYPE", "value" = ven_info.device_type},
            {"name" = "TIMEZONE", "value" = ven_info.timezone},
            {"name" = "PRICE_THRESHOLD", "value" = ven_info.price_threshold},
            {"name" = "INTERVAL_OF_FETCHING_DEVICE_DATA_INSECOND", "value" = ven_info.interval_of_fetching_device_data_insecond},
            {"name" = "REPORT_DURATION_INSECOND", "value" = ven_info.report_duration_insecond},
            {"name" =  "REPORT_SPECIFIER_ID", "value" = ven_info.report_specifier_id},
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
                "awslogs-group" = ven_log_group_name,
                "awslogs-region" = log_group_region,
                "awslogs-stream-prefix": "ven"
            }
        },
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/ven",
                "sourceVolume": "ven-volume"
            }
        ]
    }
])}

