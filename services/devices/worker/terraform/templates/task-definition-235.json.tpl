[
    {
        "name": "vtn-235",
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
                "value": "235"
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
                "containerPath": "/vol/vtn-235",
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
                "awslogs-stream-prefix": "235-vtn-235"
            }
        }
    }
]