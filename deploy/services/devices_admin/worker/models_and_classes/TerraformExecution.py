import subprocess
from typing import List, Dict


class TerraformExecution:
    def __init__(self, working_dir: str, name_of_creation: str, environment_variables: Dict) -> None:
        self.working_dir = working_dir
        self.name_of_creation = name_of_creation
        self.environment_variables = environment_variables

    # create terrafrom init execution
    def terraform_init(self) -> None:
        try:
            result = subprocess.run(
                ['docker-compose', 'run', '--rm', 'terraform', 'init', '-backend-config=backend.hcl', '-reconfigure'], cwd=self.working_dir)
            # if result.returncode == 1:
            #     raise Exception(
            #         f"{self.name_of_creation}: Subprocess returned error code 1, program stopped.")
        except subprocess.CalledProcessError as e:
            raise Exception(
                f"{self.name_of_creation} Error when terrafrom init : {e}")
    # create terrafrom validate execution

    def terraform_validate(self) -> None:
        """
        terraform validate
        """
        try:
            command = ['docker-compose', 'run', '--rm',
                       'terraform', 'validate']
            result = subprocess.run(command, cwd=self.working_dir)
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
                       'terraform', 'plan', "-lock=false"]
            new_command = self._append_var(command)
            result = subprocess.run(command, cwd=self.working_dir)
        except subprocess.CalledProcessError as e:
            raise Exception(
                f" {self.name_of_creation}  Error when terrafrom plan dynamodb : {e}")

    def terraform_apply(self) -> None:
        """
        terraform apply
        """
        try:
            command = ['docker-compose', 'run', '--rm',
                       'terraform', 'apply', '-auto-approve', "-lock=false"]
            new_command = self._append_var(command)
            result = subprocess.run(new_command, cwd=self.working_dir)
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
                # for variable in self.environment_variables:
                # get key and value from the variable
                # key = list(variable.keys())[0]
                # value = variable[key]
                tf_var = f"{key}={value}"
                command.append('-var')
                command.append(tf_var)
        return command
