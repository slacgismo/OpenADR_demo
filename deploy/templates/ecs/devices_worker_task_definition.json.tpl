[
    {
        "name": "${devices_worker_name}",
        "image":"041414866712.dkr.ecr.us-east-2.amazonaws.com/devices_worker:latest",
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
            "python app.py"
        ],
        "environment": [
            {
                "name": "FIFO_SQS_URL",
                "value": "${FIFO_SQS_URL}"
            },
            {
                "name": "BACKEND_S3_BUCKET_NAME",
                "value": "${BACKEND_S3_BUCKET_NAME}"
            },
            {
                "name": "AWS_REGION",
                "value": "${AWS_REGION}"
            },
            {
                "name": "FIFO_DLQ_URL",
                "value": "${FIFO_DLQ_URL}"
            },
            {
                "name": "HEALTH_CHEKC_PORT",
                "value": "${HEALTH_CHEKC_PORT}"
            },
            {
                "name": "DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME",
                "value": "${DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME}"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${log_group_name}",
                "awslogs-region": "${log_group_region}",
                "awslogs-stream-prefix": "devices_worker"
            }
        },
         "portMappings": [
            {
                "containerPort": 8070,
                "hostPort": 8070
            }
        ],
         "healthCheck": {
            "retries": 3,
            "command": [
                "CMD-SHELL",
                "curl -f http://127.0.0.1:${HEALTH_CHEKC_PORT}/health || exit 1"
            ],
            "timeout": 5,
            "interval": 30
        }
    }
]