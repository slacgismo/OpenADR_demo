[
    {
        "name": "vtn-1bfaa4687d4a969a47e25a1ef3a85d",
        "image": "${app_image_vtn}",
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
                "value": "${environment}"
            },
            {
                "name": "AGENT_ID",
                "value": "6bba76437fb5c90a271e155bd0855083"
            },
            {
                "name": "RESOURCE_ID",
                "value": "39e641cc76436854310668976b14c851"
            },
            {
                "name": "VTN_ID",
                "value": "1bfaa4687d4a969a47e25a1ef3a85d"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECOND",
                "value": 60
            },
            {
                "name": "SAVE_DATA_URL",
                "value": "${SAVE_DATA_URL}"
            },
            {
                "name": "GET_VENS_URL",
                "value": "${GET_VENS_URL}"
            },
            {
                "name": "MARKET_PRICES_URL",
                "value": "${MARKET_PRICES_URL}"
            },
            {
                "name": "PARTICIPATED_VENS_URL",
                "value": "${PARTICIPATED_VENS_URL}"
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
                "containerPath": "/vol/1bfaa4687d4a969a47e25a1ef3a85d",
                "sourceVolume": "agent-volume"
            }
        ],
        "healthCheck": {
            "retries": 3,
            "command": [
                "CMD-SHELL",
                "curl -f http://${vtn_address}:${vtn_port}/health || exit 1"
            ],
            "timeout": 5,
            "interval": 30
        },
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${cloudwatch_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "6bba76437fb5c90a271e155bd0855083-1bfaa4687d4a969a47e25a1ef3a85d"
            }
        }
    },
    {
        "name": "ven-2b7aa5f2cc4ac8b1853448ac1459df",
        "image": "${app_image_ven}",
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
                "name": "ENV",
                "value": "${environment}"
            },
            {
                "name": "VEN_ID",
                "value": "faebd2e0d44bc68b1b77347457fe0d"
            },
            {
                "name": "AGENT_ID",
                "value": "6bba76437fb5c90a271e155bd0855083"
            },
            {
                "name": "RESOURCE_ID",
                "value": "39e641cc76436854310668976b14c851"
            },
            {
                "name": "METER_ID",
                "value": "874bb4d04146409ba6ada692c5d724"
            },
            {
                "name": "DEVICE_ID",
                "value": "21d7e31f24d64edc5159d1ce20b54409"
            },
            {
                "name": "DEVICE_NAME",
                "value": "battery_0"
            },
            {
                "name": "VTN_ADDRESS",
                "value": "${vtn_address}"
            },
            {
                "name": "VTN_PORT",
                "value": "${vtn_port}"
            },
            {
                "name": "DEVICE_TYPE",
                "value": "ES"
            },
            {
                "name": "DEVICE_PARAMS",
                "value": "{\"battery_token\": \"766c332d8f46cd9ff70ec5864c6d34\", \"battery_sn\": \"26417\", \"device_brand\": \"SONNEN_BATTERY\"}"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECOND",
                "value": 60
            },
            {
                "name": "BIDING_PRICE_THRESHOLD",
                "value": 3.9789816351366687
            },
            {
                "name": "MOCK_DEVICES_API_URL",
                "value": "${MOCK_DEVICES_API_URL}"
            }
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/2b7aa5f2cc4ac8b1853448ac1459df",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${cloudwatch_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "6bba76437fb5c90a271e155bd0855083-2b7aa5f2cc4ac8b1853448ac1459df"
            }
        }
    }
]