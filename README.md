# docker push

docker push jimmyleu76/python-openleadr-nodemon

# aws login

aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 041414866712.dkr.ecr.us-east-2.amazonaws.com

docker tag jimmyleu76/python-openleadr-nodemon:latest 041414866712.dkr.ecr.us-east-2.amazonaws.com/openleadr-vtn:latest

# install docker in ec2

# Update the installed packages and package cache on your instance.

sudo yum update -y
sudo yum install git nano -y

# Install the most recent Docker Community Edition package.sudo

amazon-linux-extras install docker

# Start the Docker service.

sudo service docker start

# Add the ec2-user to the docker group so you can execute Docker #commands without using sudo.

sudo usermod -a -G docker ec2-user

sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose version

# reference

https://github.com/robogeek/openleadr-docker-setup/blob/main/testven.py
https://github.com/robogeek/openleadr-docker-setup/blob/main/docker-compose.yml
https://techsparx.com/energy-system/openadr/openleadr-docker.html
041414866712.dkr.ecr.us-east-2.amazonaws.com/openleadr-vtn:latest
https://levelup.gitconnected.com/deploy-a-dockerized-fastapi-application-to-aws-cc757830ba1b
