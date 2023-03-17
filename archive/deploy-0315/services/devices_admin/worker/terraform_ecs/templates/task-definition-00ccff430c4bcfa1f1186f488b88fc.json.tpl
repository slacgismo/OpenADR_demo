[
    {
        "name": "vtn-dae11acdbd4790b9df940ceadd8bd4",
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
                "value": "00ccff430c4bcfa1f1186f488b88fc"
            },
            {
                "name": "RESOURCE_ID",
                "value": "caff6719c24359a155a4d0d2f265a7"
            },
            {
                "name": "VTN_ID",
                "value": "dae11acdbd4790b9df940ceadd8bd4"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECOND",
                "value": "300"
            },
            {
                "name": "SAVE_DATA_URL",
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
            },
            {
                "name": "GET_VENS_URL",
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
            },
            {
                "name": "MARKET_PRICES_URL",
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/market_prices"
            },
            {
                "name": "PARTICIPATED_VENS_URL",
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/participated_vens"
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
                "containerPath": "/vol/dae11acdbd4790b9df940ceadd8bd4",
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
                "awslogs-stream-prefix": "00ccff430c4bcfa1f1186f488b88fc-dae11acdbd4790b9df940ceadd8bd4"
            }
        }
    },
    {
        "name": "ven-c7fb76775642ecbabfda4f5e2354cc",
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
                "value": "DEV"
            },
            {
                "name": "VEN_ID",
                "value": "d66307763449139a99e5f3dc16ab76"
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
                "value": "d66307763449139a99e5f3dc16ab76"
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
                "value": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/battery_api"
            }
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/c7fb76775642ecbabfda4f5e2354cc",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "openadr-ecs-agent",
                "awslogs-region": "us-east-2",
                "awslogs-stream-prefix": "00ccff430c4bcfa1f1186f488b88fc-c7fb76775642ecbabfda4f5e2354cc"
            }
        }
    }
]