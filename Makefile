#####################################################
# Makefile containing shortcut commands for project #
#####################################################


.PHONY: tf-init
tf-init:
	docker-compose run --rm terraform -chdir=terraform init -backend-config=backend.hcl

.PHONY: tf-fmt
tf-fmt:
	docker-compose run --rm terraform -chdir=terraform fmt


.PHONY: tf-validate
tf-validate:
	docker-compose run --rm terraform -chdir=terraform validate

.PHONY: tf-plan
tf-plan:
	docker-compose run --rm terraform -chdir=terraform plan

.PHONY: tf-apply
tf-apply:
	docker-compose run --rm terraform -chdir=terraform apply --auto-approve

.PHONY: tf-destroy
tf-destroy:
	docker-compose run --rm terraform -chdir=terraform destroy --auto-approve

.PHONY: list-tf-workspace
list-tf-workspace:
	docker-compose -f deploy/docker-compose.yml run --rm terraform workspace list

.PHONY: create-tf-workspace-dev
create-tf-workspace-dev:
	docker-compose -f deploy/docker-compose.yml run --rm terraform workspace new dev

.PHONY: tf-workspace-dev
tf-workspace-dev:
	docker-compose -f deploy/docker-compose.yml run --rm terraform workspace select dev


.PHONY: tf-workspace-staging
tf-workspace-staging:
	docker-compose -f deploy/docker-compose.yml run --rm terraform workspace select staging

.PHONY: tf-workspace-prod
tf-workspace-prod:
	docker-compose -f deploy/docker-compose.yml run --rm terraform workspace select prod

.PHONY: test
test:
	echo "Implement test function"


.PHONY: login-ecr
login-ecr:
	aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 041414866712.dkr.ecr.us-east-2.amazonaws.com
	
.PHONY: tagAndPush
tagAndPush:
	docker tag services_vtn:latest 041414866712.dkr.ecr.us-east-2.amazonaws.com/vtn:latest
	docker tag services_ven:latest 041414866712.dkr.ecr.us-east-2.amazonaws.com/ven:latest
	docker push 041414866712.dkr.ecr.us-east-2.amazonaws.com/vtn:latest
	docker push 041414866712.dkr.ecr.us-east-2.amazonaws.com/ven:latest


.PHONY: docker-compose-worker-up
docker-compose-worker-up:
	docker-compose -f docker-compose.worker.yml up 

.PHONY: docker-compose-openadr-up
docker-compose-openadr-up:
	docker-compose -f docker-compose.openadr.yml up 