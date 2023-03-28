
# =================================================================================================
#   Agents exec role amd iam role
# =================================================================================================


resource "aws_iam_policy" "task_execution_role_policy" {
  name        = "${var.prefix}-task-exec-role-policy"
  path        = "/"
  description = "Allow retrieving images and adding to logs"
  policy      = file("./templates/ecs/agents/task-exec-role.json")
}
# Agent exec role
resource "aws_iam_role" "task_execution_role" {
  name               = "${var.prefix}-${var.client}-${var.environment}-agent-exec-role"
  assume_role_policy = file("./templates/ecs/assume-role-policy.json")
  tags               = local.common_tags
}

resource "aws_iam_role_policy_attachment" "task_execution_role" {
  role       = aws_iam_role.task_execution_role.name
  policy_arn = aws_iam_policy.task_execution_role_policy.arn
}



resource "aws_iam_role" "app_iam_role" {
  name               = "${var.prefix}-${var.client}-${var.environment}-agent-iam-role"
  assume_role_policy = file("./templates/ecs/assume-role-policy.json")

  tags = local.common_tags
}



# =================================================================================================
#   Device worker exec role
# =================================================================================================

data "template_file" "devices_workers_execution_role_file" {
  template = file("./templates/ecs/worker/devices-work-exec-role.json.tpl")
}
resource "aws_iam_policy" "device_workers_execution_role_policy" {
  name = "${var.prefix}-${var.client}-${var.environment}-device-worker-exec-role"
  # name        = "${var.prefix}-device-workers-exec-role-policy"
  path        = "/"
  description = "Allow retrieving images and adding to logs"
  policy      = data.template_file.devices_workers_execution_role_file.rendered
}
# Agent exec role
resource "aws_iam_role" "device_workers_execution_role" {
  name               = "${var.prefix}-device-workers-exec-role"
  assume_role_policy = file("./templates/ecs/assume-role-policy.json")
  tags               = local.common_tags
}

resource "aws_iam_role_policy_attachment" "device_worker_execution_role" {
  role       = aws_iam_role.device_workers_execution_role.name
  policy_arn = aws_iam_policy.device_workers_execution_role_policy.arn
}



# =================================================================================================
# Device worker IAM role
# =================================================================================================

resource "aws_iam_role" "devices_workers_iam_role" {
  name = "${var.prefix}-${var.client}-${var.environment}-device-worker-iam-role"
  # name               = "${var.prefix}-${var.device_worker_role_name}"
  assume_role_policy = file("./templates/ecs/assume-role-policy.json")

  tags = local.common_tags
}




# =================================================================================================
# S3 policy and attachment
# =================================================================================================
data "template_file" "workers_s3_policy_file" {
  template = file("./templates/ecs/worker/s3_policy.json.tpl")
  vars = {
    backend_s3_bucket_agents_name = aws_s3_bucket.device_shared.bucket
    backend_s3_bucket_main_name   = var.backend_main_s3_bucket
  }
}

resource "aws_iam_policy" "device_worker_s3_policy" {
  name        = "${var.prefix}-${var.client}-${var.environment}-s3-policy"
  path        = "/"
  description = "Allow retrieving images and adding to logs"
  policy      = data.template_file.workers_s3_policy_file.rendered
}

resource "aws_iam_role_policy_attachment" "s3_attachment" {
  policy_arn = aws_iam_policy.device_worker_s3_policy.arn
  role       = aws_iam_role.devices_workers_iam_role.name
}

# =================================================================================================
# SQS policy and attachment
# =================================================================================================


data "template_file" "workers_sqs_policy_file" {
  template = file("./templates/ecs/worker/sqs_policy.json.tpl")
  vars = {
    fifo_sqs_arn     = aws_sqs_queue.worker_dlq.arn
    fifo_dlq_sqs_arn = aws_sqs_queue.opneadr_workers_sqs.arn
  }
}

resource "aws_iam_policy" "device_worker_sqs_policy" {
  name        = "${var.prefix}-${var.client}-${var.environment}-sqs-policy"
  path        = "/"
  description = "Allow retrieving images and adding to logs"
  policy      = data.template_file.workers_sqs_policy_file.rendered
}

resource "aws_iam_role_policy_attachment" "sqs_attachment" {
  policy_arn = aws_iam_policy.device_worker_sqs_policy.arn
  role       = aws_iam_role.devices_workers_iam_role.name
}

# =================================================================================================
# Dynamodb policy and attachment
# =================================================================================================

data "template_file" "workers_dynamodb_policy_file" {
  template = file("./templates/ecs/worker/dynamodb_policy.json.tpl")
  vars = {
    dynamodb_agents_shared_remote_state_lock_table_arn = aws_dynamodb_table.agenets_shared_state_lock.arn
  }
}

resource "aws_iam_policy" "device_worker_dynamodb_policy" {
  name        = "${var.prefix}-${var.client}-${var.environment}-dynamodb-policy"
  path        = "/"
  description = "Allow retrieving images and adding to logs"
  policy      = data.template_file.workers_dynamodb_policy_file.rendered
}

resource "aws_iam_role_policy_attachment" "dynamodb_attachment" {
  policy_arn = aws_iam_policy.device_worker_dynamodb_policy.arn
  role       = aws_iam_role.devices_workers_iam_role.name
}


# =================================================================================================
# Iam role policy and attachment
# =================================================================================================
data "template_file" "workers_iam_policy_file" {
  template = file("./templates/ecs/worker/iam_policy.json.tpl")
}

resource "aws_iam_policy" "devices_workers_iam_policy" {
  name        = "${var.prefix}-${var.client}-${var.environment}-iam-policy"
  path        = "/"
  description = "Allow retrieving images and adding to logs"
  policy      = data.template_file.workers_iam_policy_file.rendered
}

resource "aws_iam_role_policy_attachment" "iam_attachment" {
  policy_arn = aws_iam_policy.devices_workers_iam_policy.arn
  role       = aws_iam_role.devices_workers_iam_role.name
}
# =================================================================================================
# Logs policy and attachment
# =================================================================================================

data "template_file" "workers_log_policy_file" {
  template = file("./templates/ecs/worker/log_policy.json.tpl")
  vars = {
    cloud_watch_agent_log_group_arn = aws_cloudwatch_log_group.agent_task_logs.arn
    account_id                      = data.aws_caller_identity.current.account_id
  }
}

resource "aws_iam_policy" "device_worker_log_policy" {
  name        = "${var.prefix}-${var.client}-${var.environment}-log-policy"
  path        = "/"
  description = "Allow retrieving images and adding to logs"
  policy      = data.template_file.workers_log_policy_file.rendered
}

resource "aws_iam_role_policy_attachment" "log_attachment" {
  policy_arn = aws_iam_policy.device_worker_log_policy.arn
  role       = aws_iam_role.devices_workers_iam_role.name
}


# =================================================================================================
# EC2 policy and attachment
# =================================================================================================

data "template_file" "workers_ec2_policy_file" {
  template = file("./templates/ecs/worker/ec2_policy.json.tpl")
}

resource "aws_iam_policy" "device_worker_ec2_policy" {
  name        = "${var.prefix}-${var.client}-${var.environment}-ec2-policy"
  path        = "/"
  description = "Allow retrieving images and adding to logs"
  policy      = data.template_file.workers_ec2_policy_file.rendered
}

resource "aws_iam_role_policy_attachment" "ec2_attachment" {
  policy_arn = aws_iam_policy.device_worker_ec2_policy.arn
  role       = aws_iam_role.devices_workers_iam_role.name
}


# =================================================================================================
# ECS policy and attachment
# =================================================================================================

data "template_file" "workers_ecs_limit_policy_file" {
  template = file("./templates/ecs/worker/ecs_policy.json.tpl")
  vars = {
    account_id      = data.aws_caller_identity.current.account_id
    ecs_cluster_arn = aws_ecs_cluster.main.arn
  }
}

resource "aws_iam_policy" "device_worker_ecs_limit_policy" {
  name = "${var.prefix}-${var.client}-${var.environment}-ecs-policy"

  path        = "/"
  description = "Allow retrieving images and adding to logs"
  policy      = data.template_file.workers_ecs_limit_policy_file.rendered
}

resource "aws_iam_role_policy_attachment" "ecs_attachment" {
  policy_arn = aws_iam_policy.device_worker_ecs_limit_policy.arn
  role       = aws_iam_role.devices_workers_iam_role.name
}
