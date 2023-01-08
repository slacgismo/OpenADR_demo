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
sudo git clone https://github.com/slacgismo/openADR-nodemon.git /home/ec2-user/openADR
echo "start docker-compose"
# start docker-compose
cd /home/ec2-user/openADR 
docker-compose up 
