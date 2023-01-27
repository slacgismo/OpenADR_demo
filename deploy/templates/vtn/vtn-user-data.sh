#!/bin/bash

sudo yum update -y
sudo yum install git nano -y
sudo amazon-linux-extras install -y docker
sudo systemctl enable docker.service
sudo systemctl start docker.service
sudo usermod -aG docker ec2-user
# install docker-compose
echo "install docker-compose"
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
sudo docker-compose version
# git clone openadr project
# sudo mkdir home/ec2-user/openADR
echo "mkdir home/ec2-user/openADR"
sudo chmod +rwx home/ec2-user/openADR
sudo git clone https://github.com/slacgismo/OpenADR_demo.git /home/ec2-user/openADR

# start docker-compose


touch  /home/ec2-user/openADR/tmp.txt
chmod +rwx /home/ec2-user/openADR/tmp.txt
echo "============================"
echo "export DB_HOST=${DB_HOST}" | sudo tee -a /home/ec2-user/openADR/tmp.txt 
echo "export DB_USER=${DB_USER}" | sudo tee -a /home/ec2-user/openADR/tmp.txt
echo "export DB_PASSWORD=${DB_PASSWORD}" | sudo tee -a /home/ec2-user/openADR/tmp.txt
echo "export DB_NAME=${DB_NAME}" | sudo tee -a /home/ec2-user/openADR/tmp.txt
source .tmp.txt
echo "============================"
echo "start docker-compose"
cd /home/ec2-user/openADR/docker-vtn
docker-compose up 