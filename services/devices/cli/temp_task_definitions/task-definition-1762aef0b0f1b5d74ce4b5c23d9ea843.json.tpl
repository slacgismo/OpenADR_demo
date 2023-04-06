[
    {
        "name": "vtn-131a8331ae432890457e09fc5542a1",
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
                "value": "1762aef0b0f1b5d74ce4b5c23d9ea843"
            },
            {
                "name": "RESOURCE_ID",
                "value": "3b4a58e3cd70cd9c6f781d9267c6c5c0"
            },
            {
                "name": "VTN_ID",
                "value": "131a8331ae432890457e09fc5542a1"
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
                "containerPath": "/vol/131a8331ae432890457e09fc5542a1",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${cloudwatch_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "1762aef0b0f1b5d74ce4b5c23d9ea843-131a8331ae432890457e09fc5542a1"
            }
        }
    },
    {
        "name": "ven-dfd49854eb4f98883ec0813f75ab28",
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
                "value": "7fafc55dfc41f288b56133a3ef9849"
            },
            {
                "name": "AGENT_ID",
                "value": "1762aef0b0f1b5d74ce4b5c23d9ea843"
            },
            {
                "name": "RESOURCE_ID",
                "value": "3b4a58e3cd70cd9c6f781d9267c6c5c0"
            },
            {
                "name": "METER_ID",
                "value": "f3996bab614ea8999245cba4f0c4cd"
            },
            {
                "name": "DEVICE_ID",
                "value": "1eb7c1bc0cfc18a92d7f818e69790616"
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
                "value": "{\"battery_token\": \"48e4980d464ddaa7c519e1db7962f6\", \"battery_sn\": \"10001\", \"device_brand\": \"SONNEN_BATTERY\"}"
            },
            {
                "name": "MARKET_INTERVAL_IN_SECONDS",
                "value": "60"
            },
            {
                "name": "FLEXIBLE",
                "value": "3.682823271993134"
            },
            {
                "name": "EMULATED_DEVICE_API_URL",
                "value": "{$EMULATED_DEVICE_API_URL}"
            }
        ],
        "mountPoints": [
            {
                "readOnly": false,
                "containerPath": "/vol/dfd49854eb4f98883ec0813f75ab28",
                "sourceVolume": "agent-volume"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${cloudwatch_name}",
                "awslogs-region": "${aws_region}",
                "awslogs-stream-prefix": "1762aef0b0f1b5d74ce4b5c23d9ea843-dfd49854eb4f98883ec0813f75ab28"
            }
        }
    }
]