{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "s3:GetObject",
                "s3:PutObject",
                "sqs:SendMessage",
                "sqs:ReceiveMessage",
                "ecs:CreateService",
                "ecs:DeleteService",
                "dynamodb:GetItem",
                "dynamodb:PutItem"
            ],
            "Resource": [
                "*",
                "arn:aws:s3:::${backend_s3_bucket_devices_admin}/*",
                "arn:aws:sqs:*:*:${worker_fifo_sqs_url}",
                "arn:aws:ecs:*:*:service/${ecs_cluster_name}/*",
                "arn:aws:dynamodb:*:*:table/${dynamodb_agents_shared_remote_state_lock_table_name}"
            ]
        }
    ]
}