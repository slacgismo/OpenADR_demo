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
                "*"
            ]
        }
    ]
}