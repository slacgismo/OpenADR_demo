[
    {
        "name": "vtn-341bf1a888486d9772c54500f4b4e5",
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
                "value": "3375c46d3f706ef857001f00a2e8e29b"
            },
            {
                "name": "RESOURCE_ID",
                "value": "3b4a58e3cd70cd9c6f781d9267c6c5c0"
            },
            {
                "name": "VTN_ID",
                "value": "341bf1a888486d9772c54500f4b4e5"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECOND",
                "value": "60"
            },
            {
                "name": "METER_API_URL",
                "value": "{$METER_API_URL}"
            },
            {
                "name": "DEVICE_API_URL",
                "value": "{$DEVICE_API_URL}"
            },
            {
                "name": "ORDER_PAI_URL",
                "value": "{$ORDER_PAI_URL}"
            },
            {
                "name": "DISPATCH_API_URL",
                "value": "{$DISPATCH_API_URL}"
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
                "containerPath": "/vol/341bf1a888486d9772c54500f4b4e5",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${cloudwatch_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "3375c46d3f706ef857001f00a2e8e29b-341bf1a888486d9772c54500f4b4e5"
            }
        }
    },
    {
        "name": "ven-ee47744ab9475bba61d0941adeb82c",
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
                "value": "459006ab9346cdb0bb32b5d574bb3a"
            },
            {
                "name": "AGENT_ID",
                "value": "3375c46d3f706ef857001f00a2e8e29b"
            },
            {
                "name": "RESOURCE_ID",
                "value": "3b4a58e3cd70cd9c6f781d9267c6c5c0"
            },
            {
                "name": "METER_ID",
                "value": "7c93c42bad4814a894212f614ba396"
            },
            {
                "name": "DEVICE_ID",
                "value": "3b33359b7a276727449459ab65f020de"
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
                "name": "DEVICE_SETTINGS",
                "value": "{\"battery_token\": \"73d34ed63a48349f047a5bc85141c6\", \"battery_sn\": \"65169\", \"device_brand\": \"SONNEN_BATTERY\"}"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECOND",
                "value": "60"
            },
            {
                "name": "BIDING_PRICE_THRESHOLD",
                "value": "5.3705144724777165"
            },
            {
                "name": "EMULATED_DEVICE_API_URL",
                "value": "{$EMULATED_DEVICE_API_URL}"
            }
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/ee47744ab9475bba61d0941adeb82c",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${cloudwatch_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "3375c46d3f706ef857001f00a2e8e29b-ee47744ab9475bba61d0941adeb82c"
            }
        }
    }
]