#####################################################
# Makefile containing shortcut commands for project #
#####################################################


.PHONY: test
test:
	echo "Implement test function"


.PHONY: login-ecr
login-ecr:
	aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 041414866712.dkr.ecr.us-east-2.amazonaws.com
	
.PHONY: tagAndPush
tagAndPush:
	docker tag devices_worker:latest 041414866712.dkr.ecr.us-east-2.amazonaws.com/devices_worker:latest
	docker push 041414866712.dkr.ecr.us-east-2.amazonaws.com/devices_worker:latest