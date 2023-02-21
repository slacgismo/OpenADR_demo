[
    {
        "name": "ven",
        "image": "${app_image}",
        "essential": true,
        "memoryReservation": 256,
        "environment": [
            {"name": "VEN_NAME", "value": "${ven_name}"},
            {"name": "VTN_URL", "value": "${vtn_url}"},
            {"name": "BATTERY_TOKEN", "value": "${battery_token}"},
            {"name": "BATTERY_SN", "value": "${battery_sn}"},
            {"name": "DEVICE_ID", "value": "${device_id}"},
            {"name": "DEVICE_TYPE", "value": "${device_type}"},
            {"name": "TIMEZONE", "value": "${timezone}"},
            {"name": "PRICE_THRESHOLD", "value": "${price_threshold}"}
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
                "awslogs-group": "${log_group_name}",
                "awslogs-region": "${log_group_region}",
                "awslogs-stream-prefix": "ven"
            }
        }
    }
]
