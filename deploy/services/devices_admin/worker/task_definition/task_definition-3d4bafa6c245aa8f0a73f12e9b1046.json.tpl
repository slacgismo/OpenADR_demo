[
    {
        "name": "vtn-9e7c13885c4f7db389b83ce53d8eff",
        "image": [
            "041414866712.dkr.ecr.us-east-2.amazonaws.com/vtn:latest"
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
                "name": "ENV",
                "value": "DEV"
            },
            {
                "name": "AGENT_ID",
                "value": "3d4bafa6c245aa8f0a73f12e9b1046"
            },
            {
                "name": "VTN_ID",
                "value": "9e7c13885c4f7db389b83ce53d8eff"
            },
            {
                "name": "RESOURCE_ID",
                "value": "1c90ba71634ed5a3f4d9be9e7d6c35"
            },
            {
                "name": "APP_IMAGE_VTN",
                "value": [
                    "041414866712.dkr.ecr.us-east-2.amazonaws.com/vtn:latest"
                ]
            },
            {
                "name": "SAVE_DATA_URL",
                "value": "127.0.0.1"
            },
            {
                "name": "GET_VENS_URL",
                "value": "https: // l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
            },
            {
                "name": "MARKET_PRICES_URL",
                "value": "https: // l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/market_prices"
            },
            {
                "name": "PARTICIPATED_VENS_URL",
                "value": "https: // l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/participated_vens"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECOND",
                "value": "300"
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
                "containerPath": "/vol/9e7c13885c4f7db389b83ce53d8eff",
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
                "awslogs-group": "openadr-ecs-agent",
                "awslogs-region": "us-east-2",
                "awslogs-stream-prefix": "3d4bafa6c245aa8f0a73f12e9b1046-9e7c13885c4f7db389b83ce53d8eff"
            }
        }
    },
    {
        "name": "ven-d6d2a2a2da449d93ec73a8c7e48f39",
        "image": [
            "041414866712.dkr.ecr.us-east-2.amazonaws.com/ven:latest"
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
                "name": "ENV",
                "value": "DEV"
            },
            {
                "name": "AGENT_ID",
                "value": "3d4bafa6c245aa8f0a73f12e9b1046"
            },
            {
                "name": "VEN_ID",
                "value": "d6d2a2a2da449d93ec73a8c7e48f39"
            },
            {
                "name": "DEVICE_ID",
                "value": "862812d46c4d82afe2ac47c1f4f843"
            },
            {
                "name": "DEVICE_NAME",
                "value": "battery_0"
            },
            {
                "name": "DEVICE_TYPE",
                "value": "HS"
            },
            {
                "name": "METER_ID",
                "value": "f32240b7e0433883ee30f34d257d18"
            },
            {
                "name": "PRICE_THRESHOLD",
                "value": "0.15"
            },
            {
                "name": "APP_IMAGE_VEN",
                "value": [
                    "041414866712.dkr.ecr.us-east-2.amazonaws.com/ven:latest"
                ]
            },
            {
                "name": "MOCK_DEVICES_API_URL",
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/battery_api"
            },
            {
                "name": "DEVICE_PARAMS",
                "value": "{\"battery_token\": \"12321321qsd\", \"battery_sn\": \"66354\", \"meter_id\": \"f32240b7e0433883ee30f34d257d18\"}"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECOND",
                "value": "300"
            }
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/d6d2a2a2da449d93ec73a8c7e48f39",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "openadr-ecs-agent",
                "awslogs-region": "us-east-2",
                "awslogs-stream-prefix": "3d4bafa6c245aa8f0a73f12e9b1046-d6d2a2a2da449d93ec73a8c7e48f39"
            }
        }
    }
]