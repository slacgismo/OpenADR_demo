
# It's dynamic remote state, please create a backend.hcl
# include the following content:
# bucket         = "<your s3 state bucket>"
# key            = "<your state key>"
# region         = "<your aws region>"
# encrypt        = true
# dynamodb_table = "<your dynamodb table>" # Please create a "LockID" as a primary key

terraform {
  backend "s3" {}
}

