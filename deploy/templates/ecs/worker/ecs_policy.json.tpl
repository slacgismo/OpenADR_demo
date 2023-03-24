{
    "Version": "2012-10-17",
    "Statement": [
        {

            "Effect": "Allow",
            "Action": [
                "ecs:ListServicesByNamespace",
                "servicediscovery:ListServices",
                "ecs:DiscoverPollEndpoint",
                "ecs:PutAccountSettingDefault",
                "servicediscovery:GetOperation",
                "ecs:CreateCluster",
                "servicediscovery:ListNamespaces",
                "servicediscovery:CreateService",
                "ecs:DescribeTaskDefinition",
                "servicediscovery:UpdateService",
                "ecs:PutAccountSetting",
                "ecs:ListServices",
                "ecs:CreateCapacityProvider",
                "ecs:DeregisterTaskDefinition",
                "ecs:ListAccountSettings",
                "servicediscovery:DeleteService",
                "ecs:DeleteAccountSetting",
                "ecs:ListTaskDefinitionFamilies",
                "ecs:RegisterTaskDefinition",
                "servicediscovery:GetNamespace",
                "servicediscovery:GetService",
                "ecs:ListTaskDefinitions",
                "ecs:CreateTaskSet",
                "ecs:ListClusters"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "ecs:*",
            "Resource": [
                "arn:aws:ecs:*:${account_id}:service/*/*",
                "arn:aws:ecs:*:${account_id}:container-instance/*/*",
                "arn:aws:ecs:*:${account_id}:task-definition/*:*",
                "arn:aws:ecs:*:${account_id}:task-set/*/*/*",
                "${ecs_cluster_arn}",
                "arn:aws:ecs:*:${account_id}:task/*/*",
                "arn:aws:ecs:*:${account_id}:capacity-provider/*"
            ]
        }
    ]
}