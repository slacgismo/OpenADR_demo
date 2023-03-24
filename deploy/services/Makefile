#####################################################
# Makefile containing shortcut commands for project #
#####################################################


.PHONY: tf-init
tf-init:
	docker-compose -f deploy/docker-compose.yml run --rm terraform init -backend-config=backend.hcl

.PHONY: tf-fmt
tf-fmt:
	docker-compose -f deploy/docker-compose.yml run --rm terraform fmt

.PHONY: tf-validate
tf-validate:
	docker-compose -f deploy/docker-compose.yml run --rm terraform validate

.PHONY: tf-plan
tf-plan:
	docker-compose -f deploy/docker-compose.yml run --rm terraform plan

.PHONY: tf-apply
tf-apply:
	docker-compose -f deploy/docker-compose.yml run --rm terraform apply

.PHONY: tf-destroy
tf-destroy:
	docker-compose -f deploy/docker-compose.yml run --rm terraform destroy

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
