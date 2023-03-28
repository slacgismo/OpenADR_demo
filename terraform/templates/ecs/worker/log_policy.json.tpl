{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "LOGAccessDeviceWorker",
            "Effect": "Allow",
            "Action": [
                "logs:ListTagsLogGroup",
                "logs:CreateLogStream",
                "logs:DescribeLogGroups",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:*:${account_id}:log-group:*:log-stream:*",
                "${cloud_watch_agent_log_group_arn}"
            ]
        }
    ]
}