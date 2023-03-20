resource "aws_ecs_cluster" "main" {
  name = "${var.prefix}-${var.environment}-agents-cluster"

  tags = local.common_tags
}

resource "aws_iam_policy" "task_execution_role_policy" {
  name        = "${var.prefix}-task-exec-role-policy"
  path        = "/"
  description = "Allow retrieving images and adding to logs"
  policy      = file("./templates/ecs/task-exec-role.json")
}
# Agent exec role
resource "aws_iam_role" "task_execution_role" {
  name               = "${var.prefix}-task-exec-role"
  assume_role_policy = file("./templates/ecs/assume-role-policy.json")
  tags               = local.common_tags
}

resource "aws_iam_role_policy_attachment" "task_execution_role" {
  role       = aws_iam_role.task_execution_role.name
  policy_arn = aws_iam_policy.task_execution_role_policy.arn
}


resource "aws_iam_role" "app_iam_role" {
  name               = "${var.prefix}-vtn-task"
  assume_role_policy = file("./templates/ecs/assume-role-policy.json")

  tags = local.common_tags
}


#device worker exec role
data "template_file" "devices_worker_execution_role_file" {
  template = file("./templates/ecs/devices-work-exec-role.json.tpl")
  vars = {
    worker_fifo_sqs_url="${aws_sqs_queue.opneadr_workers_sqs.url}"
    backend_s3_bucket_devices_admin="${aws_s3_bucket.agents.bucket}"
    ecs_cluster_name="${aws_ecs_cluster.main.name}"
    dynamodb_agents_shared_remote_state_lock_table_name="${aws_dynamodb_table.agenets_shared_state_lock.name}"
  }
}
resource "aws_iam_policy" "device_worker_execution_role_policy" {
  name        = "${var.prefix}-device-worker-exec-role-policy"
  path        = "/"
  description = "Allow retrieving images and adding to logs"
  policy      = data.template_file.devices_worker_execution_role_file.rendered
}
# Agent exec role
resource "aws_iam_role" "device_worker_execution_role" {
  name               = "${var.prefix}-device-worker-exec-role"
  assume_role_policy = file("./templates/ecs/assume-role-policy.json")
  tags               = local.common_tags
}

resource "aws_iam_role_policy_attachment" "device_worker_execution_role" {
  role       = aws_iam_role.device_worker_execution_role.name
  policy_arn = aws_iam_policy.device_worker_execution_role_policy.arn
}
