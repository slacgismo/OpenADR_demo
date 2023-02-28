[
    {
        "name": "vtn",
        "image": "${app_image}",
        "essential": true,
        "memoryReservation": 256,
        "environment": [
            {"name": "TIMEZONE", "value": "${timezone}"},
            {"name": "SAVE_DATA_URL", "value": "${save_data_url}"},
            {"name": "GET_VENS_URL", "value": "${get_vens_url}"},
            {"name": "MARKET_PRICES_URL", "value": "${market_prices_url}"},
            {"name": "PARTICIPATED_VENS_URL", "value": "${participated_vens_url}"}
        ],
        "runtimePlatform": {
            "operatingSystemFamily": "LINUX",
            "cpuArchitecture": "ARM64"
        },
        "entryPoint": [ "sh", "-c" ],
        "command": [ "python vtn.py" ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${log_group_name}",
                "awslogs-region": "${log_group_region}",
                "awslogs-stream-prefix": "vtn"
            }
        },
        "portMappings": [
            {
                "containerPort": 8080,
                "hostPort": 8080
            }
        ]
    }
]
