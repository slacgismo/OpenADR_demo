resource "aws_iam_role" "market_prices_lambda_exec" {
  name = "market_prices-lambda"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "market_prices_lambda_policy" {
  role       = aws_iam_role.market_prices_lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}



resource "aws_lambda_function" "market_prices" {
  function_name = "market_prices"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_market_prices.key

  runtime = "nodejs16.x"
  handler = "function.handler"

  source_code_hash = data.archive_file.lambda_market_prices.output_base64sha256

  role = aws_iam_role.market_prices_lambda_exec.arn
}

resource "aws_cloudwatch_log_group" "market_prices" {
  name = "/aws/lambda/${aws_lambda_function.market_prices.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_market_prices" {
  type = "zip"

  source_dir  = "${path.module}/market_prices"
  output_path = "${path.module}/market_prices.zip"
}

resource "aws_s3_object" "lambda_market_prices" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "market_prices.zip"
  source = data.archive_file.lambda_market_prices.output_path

  etag = filemd5(data.archive_file.lambda_market_prices.output_path)
}