# OpenLEADR

This project demostrate how to deply [OpendLEADR](https://github.com/openleadr) server on the `EC2` instance of `AWS` through `Terraform`.

---

## Install & Step

### Installations

First, please make sure the [Docker server](https://docs.docker.com/engine/install/) is installed and running on your local machine. If you don't have the docker installed, please install the `Docker` first.

Second,download the source code from this github respository.

```
git clone https://github.com/slacgismo/openADR-nodemon
```

Third, create and activate the python virtunal environment.(User python 3.8+ version)

```
python3 -m venv venv
soruce ./venv/bin/activate
```

Intall the python dependencies.

```
pip install --upgrade pip
pip install -r docker/requirements.txt
```

### Local Test

Test the `OpenADR` server and cline in your local machine

Activate the OpendADR server through docker-compose

```
docker-compose up
```

If you see the output of your terminal as follow, the server is activate and running successfully.

```
vtn_1  | INFO:asyncio:<Server sockets=(<asyncio.TransportSocket fd=6, family=2, type=1, proto=6, laddr=('0.0.0.0', 8080)>,)> is serving
```

Activate the OpendADR client by the following command

```
python testven.py
```

### Deploy on AWS through Terraform

#### Set up the AWS credentials

Please ask the project administrator to set up the correct AWS credentials. This project is relied on `openadr-devops-tfstate` bucket on S3 and a DynamoDB `openadr-devops-tf-state-lock` table to track the deployment state.

You can use `aws configure` or [aws-vault](https://github.com/99designs/aws-vault) to set up the AWS credentials

**_Note_** : <span style="color:blue">Please use the Terraform commmand to manage all the resources that created by the Terraform command. Modify or destroy the resources manually could cause serious issues of Terraform states</span>

#### Setup the Terraform environment

In order to keep the Terraform enviroment in the same version, this project actviate the Terraform in a docker environment. Please check the `deploy/docker-compose.yml` to see the detail.

Please follow the steps to activate the Terraform

##### Terraform workspace

Create the Terraform dev workspace. This will create a `-dev` tag on all the colud resources. (This is optional)

```
make create-tf-workspace-dev
```

List all the Terraform workspaces.

```
make list-tf-workspace
```

Select the Terraform dev workspace.

```
make tf-workspace-dev
```

##### Terraform Init

This is a requirement step every time you change the Terrafrom code.

```
make tf-init
```

##### Terraform Format

This is a optinal setp to fromat the your Terraform code.

```
make tf-fmt
```

##### Terraform validation

After you change your terrafrom code, you can use this command to validate the code.

```
make tf-validate
```

##### Terraform plan

Before you really create and provision your AWS cloud resources, you can use this command to simluate the deployment in case of any issue.

```
make tf-paln
```

##### Terraform apply

You can use this command to create and provision the AWS resources.

```
make tf-apply
```

After you execute `make tf-apply`, the terraform will print out all the infomation of resources. Then it will ask you again to confirm the execution as follow.

```
Do you want to perform these actions in workspace "dev"?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value:
```

Type `yes` to execute command.

##### Public IP of The EC2

After the Terrafrom apply command completed, the terminal prints out the public ip of the EC2 instance.

```
Apply complete! Resources: 9 added, 0 changed, 0 destroyed.

Outputs:

ec2_host = "ec2-18-217-184-xxx.us-east-2.compute.amazonaws.com"
```

The public address of EC2 instance is `18.217.184.xxx`

#### Update the clinet IP

Use any code editor such as VSCode or nano to edit the `textven.py` file. When you do the local test, the `vtn_url='http://18.217.184.115:8080/OpenADR2/Simple/2.0b'`. When you do the AWS deploy test, the `vtn_url='http://18.217.184.xxx:8080/OpenADR2/Simple/2.0b'`.

After the EC2 instance is deployed on AWS, we need to wait couple minutes until the VTN server is ready. Then we activate the VEN client in the local machine by following command.

```
python testven.py
```

##### Terraform destroy

You can use this command to destroy the AWS resources that Terraform creatred.

```
make tf-destroy
```

### Sytem Diagram

![System diagram](./OpenADR.png)

#### reference

https://github.com/robogeek/openleadr-docker-setup/blob/main/testven.py
https://github.com/robogeek/openleadr-docker-setup/blob/main/docker-compose.yml
https://techsparx.com/energy-system/openadr/openleadr-docker.html
041414866712.dkr.ecr.us-east-2.amazonaws.com/openleadr-vtn:latest
https://levelup.gitconnected.com/deploy-a-dockerized-fastapi-application-to-aws-cc757830ba1b
https://jonathanserrano.medium.com/deploy-a-fastapi-app-to-production-using-docker-and-aws-ecr-928e17312445

#### timestream

https://betterprogramming.pub/deep-dive-into-amazon-timestream-data-ingestion-in-python-18c6c09accd
https://towardsdatascience.com/amazon-timestream-is-finally-released-is-it-worth-your-time-e6b7eff10867

#### Check aws cloud init log

Under the ec2 instance, we can use the following command to check the log of EC2 instance.

```
sudo cat /var/log/cloud-init-output.log
```
