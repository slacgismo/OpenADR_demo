# AWS EC2 Instance Terraform Module
# Bastion Host - EC2 Instance that will be created in VPC Public Subnet
resource "aws_iam_policy" "ec2_policy" {
  name        = "ec2_policy"
  path        = "/"
  description = "Policy to provide permission to EC2"
  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        "Effect": "Allow",
        "Action": [
                  "ecr:BatchCheckLayerAvailability",
                  "ecr:BatchGetImage",
                  "ecr:CompleteLayerUpload",
                  "ecr:GetDownloadUrlForLayer",
                  "ecr:InitiateLayerUpload",
                  "ecr:PutImage",
                  "ecr:UploadLayerPart"
        ],
        "Resource": "*"
      },
       {
          "Action": [
              "ecr:GetAuthorizationToken",
          ],
          "Effect": "Allow",
          "Resource": "*"
       }
    ]
  })
}

#Create a role
#https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role
resource "aws_iam_role" "ec2_role" {
  name = "ec2_role"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}

#Attach role to policy
#https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy_attachment
resource "aws_iam_policy_attachment" "ec2_policy_role" {
  name       = "ec2_attachment"
  roles      = [aws_iam_role.ec2_role.name]
  policy_arn = aws_iam_policy.ec2_policy.arn
}

#Attach role to an instance profile
#https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_instance_profile
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_profile"
  role = aws_iam_role.ec2_role.name
}


# module "ec2_public_test" {
#   source  = "terraform-aws-modules/ec2-instance/aws"
#   version = "2.17.0"
#   # insert the 10 required variables here
#   name = "${var.prefix}-${var.environment}-test"
#   #instance_count         = 5
#   ami           = data.aws_ami.amzlinux2.id
#   instance_type = var.instance_type
#   key_name      = var.instance_keypair
#   iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
#   #monitoring             = true
#   subnet_id              = module.vpc.public_subnets[0]
#   vpc_security_group_ids = [module.public_bastion_sg.this_security_group_id]
#   user_data = base64encode(
#     templatefile(
#       "./templates/vtn-install.sh", 
#       {
#         TIMEZONE          ="America/Los_Angeles"
#         SAVE_DATA_URL          = "https://lv55k5wqj2.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
#         GET_VENS_URL          = "https://lv55k5wqj2.execute-api.us-east-2.amazonaws.com/dev/openadr_devices"
#       } 
#     )
#   )
#   tags                   = local.common_tags
# }

