[
    {
        "name": "vtn-4b9d2112d74eb6b52443c65eee05e9",
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
                "value": "6bf2268d5a88879c5f1ccfa9c3580a4d"
            },
            {
                "name": "RESOURCE_ID",
                "value": "3b4a58e3cd70cd9c6f781d9267c6c5c0"
            },
            {
                "name": "VTN_ID",
                "value": "4b9d2112d74eb6b52443c65eee05e9"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECONDS",
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
                "containerPath": "/vol/4b9d2112d74eb6b52443c65eee05e9",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${cloudwatch_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "6bf2268d5a88879c5f1ccfa9c3580a4d-4b9d2112d74eb6b52443c65eee05e9"
            }
        }
    },
    {
        "name": "ven-31c185524e480998b0cb1f4a274a11",
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
                "value": "56b013e75e4ffe872c63adbfd83700"
            },
            {
                "name": "AGENT_ID",
                "value": "6bf2268d5a88879c5f1ccfa9c3580a4d"
            },
            {
                "name": "RESOURCE_ID",
                "value": "3b4a58e3cd70cd9c6f781d9267c6c5c0"
            },
            {
                "name": "METER_ID",
                "value": "44db3aa77549ee88d9ad925127d6cd"
            },
            {
                "name": "DEVICE_ID",
                "value": "4d475074e704799039e36ed22c100e77"
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
                "value": "{\"battery_token\": \"abffc88ffe4d77a466bd480d350f9c\", \"battery_sn\": \"21511\", \"device_brand\": \"SONNEN_BATTERY\"}"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECONDS",
                "value": "60"
            },
            {
                "name": "FLEXIBLE",
                "value": "8.245846977826211"
            },
            {
                "name": "EMULATED_DEVICE_API_URL",
                "value": "{$EMULATED_DEVICE_API_URL}"
            }
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/31c185524e480998b0cb1f4a274a11",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${cloudwatch_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "6bf2268d5a88879c5f1ccfa9c3580a4d-31c185524e480998b0cb1f4a274a11"
            }
        }
    }
]