
from process_acitons.create_backend_hcl_file import create_backend_hcl_file
import os


def test_create_backend_hcl_file(tmp_path):
    backend_hcl_filename = "backend.hcl"
    backend_s3_bucket = "my-bucket"
    backend_s3_key = "terraform/state"
    backend_region = "us-east-1"
    backend_dynamodb_table = "terraform-state-lock"

    create_backend_hcl_file(
        path=tmp_path,
        backend_hcl_filename=backend_hcl_filename,
        backend_s3_bucket=backend_s3_bucket,
        backend_s3_key=backend_s3_key,
        backend_region=backend_region,
        backend_dynamodb_table=backend_dynamodb_table
    )

    backend_hcl_file_path = os.path.join(tmp_path, backend_hcl_filename)
    assert os.path.exists(backend_hcl_file_path)

    with open(backend_hcl_file_path, "r") as f:
        content = f.read()

    assert f'bucket         = "{backend_s3_bucket}"\n' in content
    assert f'key            = "{backend_s3_key}"\n' in content
    assert f'region         = "{backend_region}"\n' in content
    assert 'encrypt        = true\n' in content
    assert f'dynamodb_table = "{backend_dynamodb_table}"\n' in content
