[
    {
        "name": "vtn-vtn0",
        "image": "041414866712.dkr.ecr.us-east-2.amazonaws.com/vtn:latest",
        "essential": true,
        "memoryReservation": 256,
        "runtimePlatform": {
            "operatingSystemFamily": "LINUX",
            "cpuArchitecture": "ARM64"
        },
        "entryPoint": [
            "sh",
            "-c"
        ],
        "command": [
            "python vtn.py"
        ],
        "environment": [
            {
                "name": "ENV",
                "value": "DEV"
            },
            {
                "name": "VTN_ID",
                "value": "vtn0"
            },
            {
                "name": "SAVE_DATA_URL",
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
            },
            {
                "name": "GET_VENS_URL",
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
            },
            {
                "name": "MARKET_PRICES_URL",
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/market_prices"
            },
            {
                "name": "PARTICIPATED_VENS_URL",
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/participated_vens"
            },
            {
                "name": "INTERVAL_OF_FETCHING_MARKET_PRICE_INSECOND",
                "value": "20"
            }
        ],
        "portMappings": [
            {
                "containerPort": 8080,
                "hostPort": 8080
            }
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/vtn0",
                "sourceVolume": "agent-volume"
            }
        ],
        "healthCheck": {
            "retries": 3,
            "command": [
                "CMD-SHELL",
                "curl -f http://127.0.0.1:8080/health || exit 1"
            ],
            "timeout": 5,
            "interval": 30
        },
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${log_group_name}",
                "awslogs-region": "${log_group_region}",
                "awslogs-stream-prefix": "vtn0"
            }
        }
    },
    {
        "name": "ven-ven0",
        "image": "041414866712.dkr.ecr.us-east-2.amazonaws.com/ven:latest",
        "essential": true,
        "memoryReservation": 256,
        "runtimePlatform": {
            "operatingSystemFamily": "LINUX",
            "cpuArchitecture": "ARM64"
        },
        "entryPoint": [
            "sh",
            "-c"
        ],
        "command": [
            "python ven.py"
        ],
        "environment": [
            {
                "name": "VEN_ID",
                "value": "ven0"
            },
            {
                "name": "ENV",
                "value": "DEV"
            },
            {
                "name": "VTN_ADDRESS",
                "value": "127.0.0.1"
            },
            {
                "name": "VTN_PORT",
                "value": "8080"
            },
            {
                "name": "MOCK_DEVICES_API_URL",
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/battery_api"
            },
            {
                "name": "BATTERY_TOKEN",
                "value": "12321321qsd"
            },
            {
                "name": "BATTERY_SN",
                "value": "66354"
            },
            {
                "name": "DEVICE_ID",
                "value": "device_0"
            },
            {
                "name": "DEVICE_TYPE",
                "value": "SONNEN_BATTERY"
            },
            {
                "name": "PRICE_THRESHOLD",
                "value": "0.15"
            },
            {
                "name": "INTERVAL_OF_FETCHING_DEVICE_DATA_INSECOND",
                "value": "10"
            }
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/ven0",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${log_group_name}",
                "awslogs-region": "${log_group_region}",
                "awslogs-stream-prefix": "ven0"
            }
        }
    }
]