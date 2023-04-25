
# Create the shared lkayer package

data "archive_file" "lambda_shared_layers" {
  type = "zip"
  # create virtual environment
  # activate virtual environment and install packages
  # Delete the bin and include directory
  # create an empty directory name python. It is mandatory to name the directory “python”.
  # move lib and custom function to python directory
  source_dir  = "${path.module}/api/sharedLayers"
  output_path = "${path.module}/templates/shared_layers.zip"
}


resource "aws_s3_object" "lambda_shared_layers" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "shared_layers.zip"
  source = data.archive_file.lambda_shared_layers.output_path

  etag = filemd5(data.archive_file.lambda_shared_layers.output_path)
}


resource "aws_lambda_layer_version" "shared_layers" {
  compatible_runtimes = ["python3.9", "python3.8", "python3.7"] 
  layer_name = "${var.prefix}-${var.client}-${var.environment}-shared-layers"
  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_shared_layers.key

  source_code_hash   = data.archive_file.lambda_shared_layers.output_base64sha256
}


