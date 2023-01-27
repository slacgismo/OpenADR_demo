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
sudo git clone -b deploy_db https://github.com/slacgismo/openADR-nodemon.git /home/ec2-user/openADR
echo "start docker-compose"
# start docker-compose
cd /home/ec2-user/openADR/docker-vtn
# docker-compose up 
touch  home/ec2-user/openADR/tmp.txt
chmod +rwx home/ec2-user/openADR/tmp.txt
echo "DB_HOST = ${DB_HOST}" >> home/ec2-user/openADR/tmp.txt
echo "DB_USER = ${DB_USER}" >> home/ec2-user/openADR/tmp.txt
echo "DB_PASSWORD = ${DB_PASSWORD}" >> home/ec2-user/openADR/tmp.txt
echo "DB_NAME = ${DB_NAME}" >> home/ec2-user/openADR/tmp.txt