import subprocess
from typing import List, Dict
import os
import logging
import shutil


class TerraformExecution:
    def __init__(self,
                 working_dir: str = None,
                 name_of_creation: str = None,
                 environment_variables: Dict = None,
                 backend_s3_bucket_name: str = None,
                 backend_s3_state_key: str = None,
                 backend_region: str = None,
                 DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME: str = None,

                 ) -> None:
        self.working_dir = working_dir
        self.name_of_creation = name_of_creation
        self.environment_variables = environment_variables
        self.backend_s3_bucket_name = backend_s3_bucket_name
        self.backend_s3_state_key = backend_s3_state_key
        self.backend_region = backend_region
        self.DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME = DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME

        # self.lock = True  # always lock the backend state file, in case of multiple agents running at the same time
        self.use_docker_compose = False
        self.docker_compose_command = ["docker-compose", "run", "--rm"]
        self.lock = True
        if self.backend_s3_state_key is not None and DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME is not None:
            # create backend.hcl file
            self._create_backend_hcl_file()

    def _remove_terraform_tmp_file(self):
        # chk if .terraform folder exists
        # remove .terraform folder

        _terraform_folder = os.path.join(self.working_dir, ".terraform")
        if os.path.exists(_terraform_folder):
            remove_directory_contents(
                directory=_terraform_folder
            )
            logging.info("removed .terraform folder")
        logging.info("no .terraform path found")
        # chk if .terraform.lock.hcl file exists
        terraform_lock_hcl_file = os.path.join(
            self.working_dir, ".terraform.lock.hcl")
        # remove .terraform.lock.hcl
        if os.path.exists(terraform_lock_hcl_file):
            os.remove(terraform_lock_hcl_file)
            logging.info("removed .terraform.lock.hcl file")
        logging.info("no .terraform.lock.hcl file found")

    def _create_backend_hcl_file(self):
        """
        Create backend.hcl file to store the backend state key and dynamodb table name
        """
        try:
            # remove .terraform folder and .terraform.lock.hcl file

            os.makedirs(self.working_dir, exist_ok=True)

            backend_hcl_file_path = os.path.join(
                self.working_dir, "backend.hcl")
            with open(backend_hcl_file_path, "w") as f:
                f.write(f'bucket         = "{self.backend_s3_bucket_name}"\n')
                f.write(f'key            = "{self.backend_s3_state_key}"\n')
                f.write(f'region         = "{self.backend_region}"\n')
                f.write(f'encrypt        = false\n')
                f.write(
                    f'dynamodb_table = "{self.DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME}"\n')
            logging.info("--backend.hcl file created--")
            logging.info(f"--bucket =  {self.backend_s3_bucket_name}")
            logging.info(f"--key =  {self.backend_s3_state_key}")
            logging.info(f"--region = {self.backend_region}")
            logging.info("--encrypt = false")
            logging.info(
                f"--dynamodb_table = {self.DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME}")

        except Exception as e:
            raise Exception(f"Error creating backend.hcl file: {e}")

    # create terrafrom init execution

    def terraform_init(self) -> None:
        try:
            self._remove_terraform_tmp_file()

            command = ['terraform', 'init',
                       '-backend-config=backend.hcl', "-reconfigure"]
            if self.use_docker_compose:
                command = self.docker_compose_command + command
            # Alywas run terraform init with -reconfigure, since the backend config file is created after the first init
            # The local /.terraform/terraform.tfstate file need to be changed after we change the backend config file

            result = subprocess.run(
                command, cwd=self.working_dir)

            if result.returncode == 1:
                raise Exception(
                    f"{self.name_of_creation}: Subprocess returned error code 1, program stopped.")

        except subprocess.CalledProcessError as e:
            raise Exception(
                f"{self.name_of_creation} Error when terrafrom init : {e}")
    # create terrafrom validate execution

    def terraform_validate(self) -> None:
        """
        terraform validate
        """
        try:
            command = ['terraform', 'validate']
            if self.use_docker_compose:
                command = self.docker_compose_command + command
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

        logging.info("*** terraform plan ****")

        try:
            command = ['terraform', 'plan']
            if self.use_docker_compose:
                command = self.docker_compose_command + command
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
            command = ['terraform', 'apply', '-auto-approve']
            if self.use_docker_compose:
                command = self.docker_compose_command + command
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
            command = ['terraform', 'destroy', '-auto-approve']
            if self.use_docker_compose:
                command = self.docker_compose_command + command
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

        # if lock is false, append the lock flag to the command
        if self.lock == False:
            logging.warning("*** terraform -lock=false ****")
            command.append("-lock=false")

        if len(self.environment_variables) > 0:

            # loop the environment variables and append them to the command
            for key, value in self.environment_variables.items():
                tf_var = f"{key}={value}"
                command.append('-var')
                command.append(tf_var)
        return command


def remove_directory_contents(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
