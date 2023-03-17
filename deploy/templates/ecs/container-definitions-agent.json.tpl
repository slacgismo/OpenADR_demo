[
    {
        "name": "vtn",
        "image": "${app_image_vtn}",
        "essential": true,
        "memoryReservation": 256,
        "environment": [
            {"name": "VTN_ID", "value": "${vtn_id}"},
            {"name": "SAVE_DATA_URL", "value": "${save_data_url}"},
            {"name": "GET_VENS_URL", "value": "${get_vens_url}"},
            {"name": "MARKET_PRICES_URL", "value": "${market_prices_url}"},
            {"name": "PARTICIPATED_VENS_URL", "value": "${participated_vens_url}"},
            {"name": "INTERVAL_OF_FETCHING_MARKET_PRICE_INSECOND", "value": "${interval_of_fetching_market_price_insecond}"}
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
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/vtn",
                "sourceVolume": "agent-volume"
            }
        ]
    },
    {
        "name": "ven",
        "image": "${app_image_ven}",
        "essential": true,
        "memoryReservation": 256,
        "environment": [
            {"name" : "ENV", "value" : "${env}"},
            {"name" : "VEN_ID", "value" : "${ven_id}"},
            {"name" :  "VTN_URL", "value" : "${vtn_url}"},
            {"name" : "MOCK_DEVICES_API_URL", "value" : "${mock_battery_api_url}"},
            {"name" : "BATTERY_TOKEN", "value" : "${battery_token}"},
            {"name" :  "BATTERY_SN", "value" : "${battery_sn}"},
            {"name" : "DEVICE_ID", "value" : "${device_id}"},
            {"name" : "DEVICE_TYPE", "value" : "${device_type}"},
            {"name" : "PRICE_THRESHOLD", "value" : "${price_threshold}"},
            {"name" : "INTERVAL_OF_FETCHING_DEVICE_DATA_INSECOND", "value" : "${interval_of_fetching_device_data_insecond}"},
            {"name" :  "REPORT_SPECIFIER_ID", "value" : "{report_specifier_id}"}
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
        },
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/ven",
                "sourceVolume": "agent-volume"
            }
        ]
    }
]
