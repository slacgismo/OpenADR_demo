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
            },
            {
                "name": "ECS_CLUSTER_NAME",
                "value": "${ECS_CLUSTER_NAME}"
            },
            {
                "name": "WORKER_PORT",
                "value": "${WORKER_PORT}"
            },
            {
                "name": "ENV",
                "value": "${ENV}"
            },
            {
                "name": "SQS_GROUPID",
                "value": "${SQS_GROUPID}"
            }
        ],
        "HealthCheck":{
            "retries": 3,
            "command": [
                "CMD-SHELL",
                "curl -f http://localhost:${WORKER_PORT}/health || exit 1"

            ],
            "timeout": 5,
            "interval": 30
        },
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${log_group_name}",
                "awslogs-region": "${log_group_region}",
                "awslogs-stream-prefix": "devices_worker"
            }
        }
    }
]