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
                "name": "AGENT_ID",
                "value": "agent_0"
            },
            {
                "name": "RESOURCE_ID",
                "value": "resource0"
            },
            {
                "name": "VTN_ID",
                "value": "vtn0"
            },
            {
                "name": "METER_API_URL",
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
            },
            {
                "name": "DEVICE_API_URL",
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
            },
            {
                "name": "ORDER_PAI_URL",
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/market_prices"
            },
            {
                "name": "DISPATCH_API_URL",
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/participated_vens"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECOND",
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
                "name": "ENV",
                "value": "ENV"
            },
            {
                "name": "VEN_ID",
                "value": "c3a674e2b34a1db47136006c2fe880"
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
                "value": "e8dea3ba0c4a87ba7a926b57315570"
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
                "value": "127.0.0.1"
            },
            {
                "name": "VTN_PORT",
                "value": "8080"
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
                "value": "7.369006991348091"
            },
            {
                "name": "EMULATED_DEVICE_API_URL",
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/battery_api"
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