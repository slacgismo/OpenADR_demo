[
    {
        "name": "vtn-099ecfdb944d54bd0820ba3dcef493",
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
                "value": "bf1738e3884a079d1fd9e6c2161718"
            },
            {
                "name": "RESOURCE_ID",
                "value": "23c3b37571422a884f7701bdc5eb20"
            },
            {
                "name": "VTN_ID",
                "value": "099ecfdb944d54bd0820ba3dcef493"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECOND",
                "value": "300"
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
                "containerPath": "/vol/099ecfdb944d54bd0820ba3dcef493",
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
                "awslogs-stream-prefix": "bf1738e3884a079d1fd9e6c2161718-099ecfdb944d54bd0820ba3dcef493"
            }
        }
    },
    {
        "name": "ven-9a095faf82426a95488fd62342b11f",
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
                "value": "96493bd52540c4905150b15d5af013"
            },
            {
                "name": "AGENT_ID",
                "value": "bf1738e3884a079d1fd9e6c2161718"
            },
            {
                "name": "RESOURCE_ID",
                "value": "23c3b37571422a884f7701bdc5eb20"
            },
            {
                "name": "METER_ID",
                "value": "5e9441aa304065b16c00ef747fdf66"
            },
            {
                "name": "DEVICE_ID",
                "value": "9975365bb14d4fa1ccb81873c7848a"
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
                "value": "${MOCK_DEVICES_API_URL}"
            }
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/9a095faf82426a95488fd62342b11f",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${cloudwatch_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "bf1738e3884a079d1fd9e6c2161718-9a095faf82426a95488fd62342b11f"
            }
        }
    }
]