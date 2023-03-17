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
echo "export VTN_URL=${VTN_URL}" | sudo tee -a /home/ec2-user/openADR/tmp.txt 
echo "export VEN_NAME=${VEN_NAME}" | sudo tee -a /home/ec2-user/openADR/tmp.txt
echo "export BATTERY_TOKEN=${BATTERY_TOKEN}" | sudo tee -a /home/ec2-user/openADR/tmp.txt
echo "export BATTERY_SN=${BATTERY_SN}" | sudo tee -a /home/ec2-user/openADR/tmp.txt
echo "export DEVICE_ID=${DEVICE_ID}" | sudo tee -a /home/ec2-user/openADR/tmp.txt
echo "export DEVICE_TYPE=${DEVICE_TYPE}" | sudo tee -a /home/ec2-user/openADR/tmp.txt
echo "export PRICE_THRESHOLD=${PRICE_THRESHOLD}" | sudo tee -a /home/ec2-user/openADR/tmp.txt

cd /home/ec2-user/openADR
source ./tmp.txt
echo "============================"
echo "start docker-compose"
cd /home/ec2-user/openADR
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 041414866712.dkr.ecr.us-east-2.amazonaws.com
docker-compose -f ./services/ven/docker-compose.yml up