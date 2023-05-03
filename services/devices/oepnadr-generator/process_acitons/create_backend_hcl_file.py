import os


def create_backend_hcl_file(
        path: str,
        backend_hcl_filename: str,
        backend_s3_bucket: str,
        backend_s3_key: str,
        backend_region: str,
        backend_dynamodb_table: str):
    """
    Create backend.hcl file to store the backend state key and dynamodb table name
    """
    try:
        os.makedirs(path, exist_ok=True)

        backend_hcl_file_path = os.path.join(path, backend_hcl_filename)
        with open(backend_hcl_file_path, "w") as f:
            f.write(f'bucket         = "{backend_s3_bucket}"\n')
            f.write(f'key            = "{backend_s3_key}"\n')
            f.write(f'region         = "{backend_region}"\n')
            f.write(f'encrypt        = true\n')
            f.write(f'dynamodb_table = "{backend_dynamodb_table}"\n')
    except Exception as e:
        raise Exception(f"Error creating backend.hcl file: {e}")
