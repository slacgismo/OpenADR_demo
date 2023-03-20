[
    {
        "name": "vtn-855cb46a8249a5a858cc01b121086a",
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
                "value": "855cb46a8249a5a858cc01b121086a"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECOND",
                "value": "60"
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
                "containerPath": "/vol/855cb46a8249a5a858cc01b121086a",
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
                "awslogs-stream-prefix": "195728adee3af42120c157833a391249-855cb46a8249a5a858cc01b121086a"
            }
        }
    },
    {
        "name": "ven-05f46a5dfd4b1d9101c04612d3ece4",
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
                "value": "c306ca24e8430dae07aff84f588031"
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
                "value": "08f808d673480a96925129c4a18d83"
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
                "name": "DEVICE_PARAMS",
                "value": "{\"battery_token\": \"322302bd7841beac7c407961cdec37\", \"battery_sn\": \"76097\", \"device_brand\": \"SONNEN_BATTERY\"}"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECOND",
                "value": "60"
            },
            {
                "name": "BIDING_PRICE_THRESHOLD",
                "value": "4.377902278834775"
            },
            {
                "name": "MOCK_DEVICES_API_URL",
                "value": "${MOCK_DEVICES_API_URL}"
            }
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/05f46a5dfd4b1d9101c04612d3ece4",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${cloudwatch_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "195728adee3af42120c157833a391249-05f46a5dfd4b1d9101c04612d3ece4"
            }
        }
    }
]