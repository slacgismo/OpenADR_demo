[
    {
        "name": "vtn-22",
        "image": [
            "${app_image_vtn}"
        ],
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
                "name": "ENVIRONMENT",
                "value": [
                    "${environment}"
                ]
            },
            {
                "name": "AGENT_ID",
                "value": "22"
            },
            {
                "name": "RESOURCE_ID",
                "value": "caff6719c24359a155a4d0d2f265a7"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECONDS",
                "value": "60"
            },
            {
                "name": "METER_API_URL",
                "value": [
                    "${meter_api_url}"
                ]
            },
            {
                "name": "DEVICES_API_URL",
                "value": [
                    "${devices_api_url}"
                ]
            },
            {
                "name": "ORDERS_API_URL",
                "value": [
                    "${orders_api_url}"
                ]
            },
            {
                "name": "DISPATCHES_API_URL",
                "value": [
                    "${dispatches_api_url}"
                ]
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
                "containerPath": "/vol/vtn-22",
                "sourceVolume": "agent-volume"
            }
        ],
        "healthCheck": {
            "retries": 3,
            "command": [
                "CMD-SHELL",
                "curl -f http://('${vtn_address}',):('${vtn_port}',)/health || exit 1"
            ],
            "timeout": 5,
            "interval": 30
        },
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": [
                    "${cloudwatch_name}"
                ],
                "awslogs-region": [
                    "${aws_region}"
                ],
                "awslogs-stream-prefix": "22-vtn-22"
            }
        }
    },
    {
        "name": "ven-37a6d01bf4009ae512d640ac594856d3",
        "image": [
            "${app_image_ven}"
        ],
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
                "name": "ENVIRONMENT",
                "value": [
                    "${environment}"
                ]
            },
            {
                "name": "AGENT_ID",
                "value": "22"
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
                "value": "37a6d01bf4009ae512d640ac594856d3"
            },
            {
                "name": "DEVICE_TYPE",
                "value": "ES"
            },
            {
                "name": "DEVICE_SETTINGS",
                "value": "{\"battery_token\": \"12321321qsd\", \"battery_sn\": \"66354\", \"device_brand\": \"SONNEN_BATTERY\", \"is_using_mock_device\": \"true\", \"flexible\": \"1\"}"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECONDS",
                "value": "60"
            },
            {
                "name": "EMULATED_DEVICE_API_URL",
                "value": [
                    "${emulated_device_api_url}"
                ]
            }
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/ven-37a6d01bf4009ae512d640ac594856d3",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": [
                    "${cloudwatch_name}"
                ],
                "awslogs-region": [
                    "${aws_region}"
                ],
                "awslogs-stream-prefix": "22-ven-37a6d01bf4009ae512d640ac594856d3"
            }
        }
    }
]