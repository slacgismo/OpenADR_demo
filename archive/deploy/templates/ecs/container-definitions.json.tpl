[
    {
        "name": "vtn",
        "image": "${app_image}",
        "essential": true,
        "memoryReservation": 256,
        "environment": [
            {"name": "DB_HOST", "value": "${db_host}"},
            {"name": "DB_NAME", "value": "${db_name}"},
            {"name": "DB_USER", "value": "${db_user}"},    
            {"name": "DB_PASSWORD", "value": "${db_pass}"}

        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${log_group_name}",
                "awslogs-region": "${log_group_region}",
                "awslogs-stream-prefix": "api"
            }
        },
        "portMappings": [
            {
                "containerPort": 8080,
                "hostPort": 8080
            }
        ]
    }
]
