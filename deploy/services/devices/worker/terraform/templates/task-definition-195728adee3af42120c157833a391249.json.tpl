[
    {
        "name": "vtn-aa5f38f3a94813a2a13651b7de8ef0",
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
                "value": "195728adee3af42120c157833a391249"
            },
            {
                "name": "RESOURCE_ID",
                "value": "3b4a58e3cd70cd9c6f781d9267c6c5c0"
            },
            {
                "name": "VTN_ID",
                "value": "aa5f38f3a94813a2a13651b7de8ef0"
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
                "containerPath": "/vol/aa5f38f3a94813a2a13651b7de8ef0",
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
                "awslogs-stream-prefix": "195728adee3af42120c157833a391249-aa5f38f3a94813a2a13651b7de8ef0"
            }
        }
    },
    {
        "name": "ven-94c4552e6243458de4bc0d29c33d4c",
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
                "value": "7bee9bfaa14f30987812bc5498b985"
            },
            {
                "name": "AGENT_ID",
                "value": "195728adee3af42120c157833a391249"
            },
            {
                "name": "RESOURCE_ID",
                "value": "3b4a58e3cd70cd9c6f781d9267c6c5c0"
            },
            {
                "name": "METER_ID",
                "value": "da33b7499d4812a7b3b92c9b7ac92d"
            },
            {
                "name": "DEVICE_ID",
                "value": "3bd3c653deee0956613cb09229e5e52a"
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
                "value": "{\"battery_token\": \"322302bd7841beac7c407961cdec37\", \"battery_sn\": \"76097\", \"device_brand\": \"SONNEN_BATTERY\"}"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECOND",
                "value": "60"
            },
            {
                "name": "BIDING_PRICE_THRESHOLD",
                "value": "4.807162070286084"
            },
            {
                "name": "EMULATED_DEVICE_API_URL",
                "value": "{$EMULATED_DEVICE_API_URL}"
            }
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/94c4552e6243458de4bc0d29c33d4c",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${cloudwatch_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "195728adee3af42120c157833a391249-94c4552e6243458de4bc0d29c33d4c"
            }
        }
    }
]