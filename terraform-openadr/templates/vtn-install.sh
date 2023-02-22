#! /bin/bash

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
echo "export TIMEZONE=${TIMEZONE}" | sudo tee -a /home/ec2-user/openADR/tmp.txt 
echo "export SAVE_DATA_URL=${SAVE_DATA_URL}" | sudo tee -a /home/ec2-user/openADR/tmp.txt
echo "export GET_VENS_URL=${GET_VENS_URL}" | sudo tee -a /home/ec2-user/openADR/tmp.txt

cd /home/ec2-user/openADR
source ./tmp.txt
echo "============================"
echo "start docker-compose"
cd /home/ec2-user/openADR
docker-compose -f ./services/vtn/docker-compose.yml up