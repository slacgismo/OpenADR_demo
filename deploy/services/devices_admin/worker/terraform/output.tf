# dynamo_db name
output "a"{
    value = "${aws_dynamodb_table.terraform_state_lock_table.name}"
}