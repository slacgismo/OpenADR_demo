[
    {
        "name": "vtn-96d05cbf4946acaf98680d2fa494b6",
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
                "value": "22183290e84bdfe43ec149a352369118"
            },
            {
                "name": "RESOURCE_ID",
                "value": "3b4a58e3cd70cd9c6f781d9267c6c5c0"
            },
            {
                "name": "VTN_ID",
                "value": "96d05cbf4946acaf98680d2fa494b6"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECONDS",
                "value": "60"
            },
            {
                "name": "METERS_API_URL",
                "value": "{$METERS_API_URL}"
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
                "containerPath": "/vol/96d05cbf4946acaf98680d2fa494b6",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${cloudwatch_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "22183290e84bdfe43ec149a352369118-96d05cbf4946acaf98680d2fa494b6"
            }
        }
    },
    {
        "name": "ven-f01d79ac4a4032a7cedf107ac5df51",
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
                "value": "e15a5f872e4e76961e48c36b45b28a"
            },
            {
                "name": "AGENT_ID",
                "value": "22183290e84bdfe43ec149a352369118"
            },
            {
                "name": "RESOURCE_ID",
                "value": "3b4a58e3cd70cd9c6f781d9267c6c5c0"
            },
            {
                "name": "METER_ID",
                "value": "7f9812993f45f59b2e2c25f8b3830e"
            },
            {
                "name": "DEVICE_ID",
                "value": "bb6b4854ff039b315f35029a3deaecf"
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
                "value": "{\"battery_token\": \"2e06b413824c9d8812d1224eb3f11d\", \"battery_sn\": \"84124\", \"device_brand\": \"SONNEN_BATTERY\"}"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECONDS",
                "value": "60"
            },
            {
                "name": "FLEXIBLE",
                "value": "4.701926428020026"
            },
            {
                "name": "EMULATED_DEVICE_API_URL",
                "value": "{$EMULATED_DEVICE_API_URL}"
            }
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/f01d79ac4a4032a7cedf107ac5df51",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${cloudwatch_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "22183290e84bdfe43ec149a352369118-f01d79ac4a4032a7cedf107ac5df51"
            }
        }
    }
]