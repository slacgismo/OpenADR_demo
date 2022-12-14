docker run -p 8080:8080 python-docker
https://github.com/robogeek/openleadr-docker-setup/blob/main/testven.py
https://github.com/robogeek/openleadr-docker-setup/blob/main/docker-compose.yml
https://techsparx.com/energy-system/openadr/openleadr-docker.html
041414866712.dkr.ecr.us-east-2.amazonaws.com/openleadr-vtn:latest

docker push jimmyleu76/python-openleadr-nodemon

aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 041414866712.dkr.ecr.us-east-2.amazonaws.com

docker tag jimmyleu76/python-openleadr-nodemon:latest 041414866712.dkr.ecr.us-east-2.amazonaws.com/openleadr-vtn:latest

https://levelup.gitconnected.com/deploy-a-dockerized-fastapi-application-to-aws-cc757830ba1b
