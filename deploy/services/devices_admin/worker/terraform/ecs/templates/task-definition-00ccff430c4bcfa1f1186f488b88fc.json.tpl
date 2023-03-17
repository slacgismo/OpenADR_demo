[
    {
        "name": "vtn-4375ee3e8c4a738893b30489255ca2",
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
                "value": "00ccff430c4bcfa1f1186f488b88fc"
            },
            {
                "name": "RESOURCE_ID",
                "value": "caff6719c24359a155a4d0d2f265a7"
            },
            {
                "name": "VTN_ID",
                "value": "4375ee3e8c4a738893b30489255ca2"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECOND",
                "value": "300"
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
                "containerPath": "/vol/4375ee3e8c4a738893b30489255ca2",
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
                "awslogs-stream-prefix": "00ccff430c4bcfa1f1186f488b88fc-4375ee3e8c4a738893b30489255ca2"
            }
        }
    },
    {
        "name": "ven-378b2d5ab94d5a8f98b478943360c3",
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
                "value": "07d27edbcf4a4bb5818fe747a6b418"
            },
            {
                "name": "AGENT_ID",
                "value": "00ccff430c4bcfa1f1186f488b88fc"
            },
            {
                "name": "RESOURCE_ID",
                "value": "caff6719c24359a155a4d0d2f265a7"
            },
            {
                "name": "METER_ID",
                "value": "6436a67e184d3694a15886215ae464"
            },
            {
                "name": "DEVICE_ID",
                "value": "07d27edbcf4a4bb5818fe747a6b418"
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
                "value": "HS"
            },
            {
                "name": "DEVICE_PARAMS",
                "value": "{\"battery_token\": \"12321321qsd\", \"battery_sn\": \"66354\", \"device_brand\": \"SONNEN_BATTERY\"}"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECOND",
                "value": "300"
            },
            {
                "name": "BIDING_PRICE_THRESHOLD",
                "value": "0.15"
            },
            {
                "name": "MOCK_DEVICES_API_URL",
                "value": "${MOCK_DEVICES_API_URL}"
            }
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/378b2d5ab94d5a8f98b478943360c3",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${cloudwatch_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "00ccff430c4bcfa1f1186f488b88fc-378b2d5ab94d5a8f98b478943360c3"
            }
        }
    }
]