[
    {
        "name": "${devices_worker_name}",
        "image": "041414866712.dkr.ecr.us-east-2.amazonaws.com/devices_worker:latest",
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
                "name": "worker_fifo_sqs_url",
                "value": "${worker_fifo_sqs_url}"
            },
            {
                "name": "backend_s3_bucket_devices_admin",
                "value": "${backend_s3_bucket_devices_admin}"
            },
            {
                "name": "aws_region",
                "value": "${aws_region}"
            },
            {
                "name": "worker_dlq_url",
                "value": "${worker_dlq_url}"
            },
            {
                "name": "ecs_cluster_name",
                "value": "${ecs_cluster_name}"
            },
            {
                "name": "dynamodb_agents_shared_remote_state_lock_table_name",
                "value": "${dynamodb_agents_shared_remote_state_lock_table_name}"
            }
        ],
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