
# Create the shared lkayer package
# data "external" "build_shared_layer" {
#   program = ["make", "build-SharedLayer"]
#   working_dir = "../api/sharedLayers"
# }

# archive the shared layer package
data "archive_file" "lambda_shared_layers" {
  # depends_on = [data.external.build_shared_layer]
  type = "zip"
  # create virtual environment
  # activate virtual environment and install packages
  # Delete the bin and include directory
  # create an empty directory name python. It is mandatory to name the directory “python”.
  # move lib and custom function to python directory
  source_dir  = "../api/sharedLayers"
 
  output_path = "${path.module}/templates/shared_layers.zip"
}


resource "aws_s3_object" "lambda_shared_layers" {
  bucket = var.meta_data_bucket_name

  key    = "sharedLayer/shared_layers.zip"
  source = data.archive_file.lambda_shared_layers.output_path

  etag = filemd5(data.archive_file.lambda_shared_layers.output_path)
}


resource "aws_lambda_layer_version" "shared_layers" {
  compatible_runtimes = ["python3.9"] 
  layer_name = "${var.prefix}-${var.client}-${var.environment}-shared-layers"
  s3_bucket = var.meta_data_bucket_name
  s3_key    = aws_s3_object.lambda_shared_layers.key

  source_code_hash   = data.archive_file.lambda_shared_layers.output_base64sha256
}


