import subprocess
from typing import List, Dict
import os


class TerraformExecution:
    def __init__(self,
                 working_dir: str = None,
                 name_of_creation: str = None,
                 environment_variables: Dict = None,
                 backend_s3_bucket_name: str = None,
                 backend_s3_state_key: str = None,
                 backend_region: str = None,
                 backend_dynamodb_lock_name: str = None,
                 ) -> None:
        self.working_dir = working_dir
        self.name_of_creation = name_of_creation
        self.environment_variables = environment_variables
        self.backend_s3_bucket_name = backend_s3_bucket_name
        self.backend_s3_state_key = backend_s3_state_key
        self.backend_region = backend_region
        self.backend_dynamodb_lock_name = backend_dynamodb_lock_name
        if self.backend_s3_state_key is not None and backend_dynamodb_lock_name is not None:
            # create backend.hcl file
            self._create_backend_hcl_file()

    def _create_backend_hcl_file(self):
        """
        Create backend.hcl file to store the backend state key and dynamodb table name
        """
        try:
            os.makedirs(self.working_dir, exist_ok=True)

            backend_hcl_file_path = os.path.join(
                self.working_dir, "backend.hcl")
            with open(backend_hcl_file_path, "w") as f:
                f.write(f'bucket         = "{self.backend_s3_bucket_name}"\n')
                f.write(f'key            = "{self.backend_s3_state_key}"\n')
                f.write(f'region         = "{self.backend_region}"\n')
                f.write(f'encrypt        = true\n')
                f.write(
                    f'dynamodb_table = "{self.backend_dynamodb_lock_name}"\n')
            print("--backend.hcl file created--")
        except Exception as e:
            raise Exception(f"Error creating backend.hcl file: {e}")

    # create terrafrom init execution

    def terraform_init(self) -> None:
        try:
            result = subprocess.run(
                ['docker-compose', 'run', '--rm', 'terraform', 'init', '-backend-config=backend.hcl'], cwd=self.working_dir)
            if result.returncode == 1:
                raise Exception(
                    f"{self.name_of_creation}: Subprocess returned error code 1, program stopped.")
        except subprocess.CalledProcessError as e:
            raise Exception(
                f"{self.name_of_creation} Error when terrafrom init : {e}")
    # create terrafrom validate execution

    # def terraform_validate_and_plan(self) -> None:
    #     """
    #     terraform validate
    #     """
    #     try:
    #         command = ['docker-compose', 'run', '--rm',
    #                    'terraform', 'validate']
    #         result = subprocess.run(command, cwd=self.working_dir)
    #         command = ['docker-compose', 'run', '--rm',
    #                    'terraform', 'plan', "-lock=false"]
    #         new_command = self._append_var(command)
    #         result = subprocess.run(command, cwd=self.working_dir)
    #     except subprocess.CalledProcessError as e:
    #         raise Exception(
    #             f" {self.name_of_creation} Error terrafrom validate dynamodb : {e}")

    def terraform_validate(self) -> None:
        """
        terraform validate
        """
        try:
            command = ['docker-compose', 'run', '--rm',
                       'terraform', 'validate']
            result = subprocess.run(command, cwd=self.working_dir)
            if result.returncode == 1:
                raise Exception(
                    f"{self.name_of_creation}: Subprocess returned error code 1, program stopped.")
        except subprocess.CalledProcessError as e:
            raise Exception(
                f" {self.name_of_creation} Error terrafrom validate dynamodb : {e}")

    # create terrafrom plan execution
    def terraform_plan(self) -> None:
        """
        terraform plan
        """
        print("terraform plan")
        try:
            command = ['docker-compose', 'run', '--rm',
                       'terraform', 'plan']
            new_command = self._append_var(command)
            result = subprocess.run(new_command, cwd=self.working_dir)
            if result.returncode == 1:
                raise Exception(
                    f"{self.name_of_creation}: Subprocess returned error code 1, program stopped.")
        except subprocess.CalledProcessError as e:
            raise Exception(
                f" {self.name_of_creation}  Error when terrafrom plan dynamodb : {e}")

    def terraform_apply(self) -> None:
        """
        terraform apply
        """
        try:
            command = ['docker-compose', 'run', '--rm',
                       'terraform', 'apply', '-auto-approve']
            new_command = self._append_var(command)
            result = subprocess.run(new_command, cwd=self.working_dir)
            if result.returncode == 1:
                raise Exception(
                    f"{self.name_of_creation}: Subprocess returned error code 1, program)")
        except subprocess.CalledProcessError as e:
            raise Exception(
                f" {self.name_of_creation}  Error when terrafrom apply: {e}")
    # terraform destroy

    def terraform_destroy(self) -> None:
        """
        terraform destroy
        """

        try:
            command = ['docker-compose', 'run', '--rm',
                       'terraform', 'destroy', '-auto-approve']
            new_command = self._append_var(command)
            result = subprocess.run(new_command, cwd=self.working_dir)
            if result.returncode == 1:
                raise Exception(
                    f"{self.name_of_creation}: Subprocess returned error code 1, program)")
        except subprocess.CalledProcessError as e:
            raise Exception(
                f" {self.name_of_creation}  Error when terrafrom destroy : {e}")

    def _append_var(self, command: List[str]) -> List[str]:
        """
        Append the environment variables to the command
        :param command: the command to append the variables to
        """
        if len(self.environment_variables) > 0:

            # loop the environment variables and append them to the command
            for key, value in self.environment_variables.items():
                tf_var = f"{key}={value}"
                command.append('-var')
                command.append(tf_var)
        return command
