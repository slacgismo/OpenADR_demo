{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObjectTagging",
                "s3:DeleteObject",
                "s3:GetObjectAttributes",
                "s3:DeleteObjectVersionTagging",
                "s3:PutObject",
                "s3:GetBucketTagging",
                "s3:PutBucketTagging",
                "s3:PutBucketVersioning",
                "s3:PutObjectVersionTagging",
                "s3:PutObjectRetention",
                "s3:GetObjectVersion",
                "s3:GetObjectVersionTagging",
                "s3:GetObjectAcl",
                "s3:GetObject"
            ],
             "Resource": [
                "arn:aws:s3:::${backend_s3_bucket_agents_name}/*",
                "arn:aws:s3:::${backend_s3_bucket_main_name}/*"
            ]
        }
    ]
}


