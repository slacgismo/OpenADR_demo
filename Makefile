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
	docker-compose run --rm terraform  -chdir=terraform workspace list

.PHONY: create-tf-workspace-dev
create-tf-workspace-dev:
	docker-compose run --rm terraform -chdir=terraform workspace new dev

.PHONY: tf-workspace-dev
tf-workspace-dev:
	docker-compose run --rm terraform -chdir=terraform workspace select dev


.PHONY: tf-workspace-staging
tf-workspace-staging:
	docker-compose run --rm terraform -chdir=terraform workspace select staging

.PHONY: tf-workspace-prod
tf-workspace-prod:
	docker-compose run --rm terraform -chdir=terraform workspace select prod

.PHONY: test
test:
	echo "Implement test function"


.PHONY: login-ecr
login-ecr:
	aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 041414866712.dkr.ecr.us-east-2.amazonaws.com
	
.PHONY: tagAndPush
tagAndPush:
	docker tag openadr_worker:latest 041414866712.dkr.ecr.us-east-2.amazonaws.com/devices_worker:latest
	docker tag openadr_vtn:latest 041414866712.dkr.ecr.us-east-2.amazonaws.com/vtn:latest
	docker tag openadr_ven:latest 041414866712.dkr.ecr.us-east-2.amazonaws.com/ven:latest
	docker push 041414866712.dkr.ecr.us-east-2.amazonaws.com/vtn:latest
	docker push 041414866712.dkr.ecr.us-east-2.amazonaws.com/ven:latest
	docker push 041414866712.dkr.ecr.us-east-2.amazonaws.com/devices_worker:latest


.PHONY: docker-compose-up help
help:
	@echo "Usage: make docker-compose-up project=<project-name>"
	@echo "Usage: make docker-compose-build project=<project-name>"
	@echo "Usage: make docker-compose-test project=<project-name>"
	@echo "Usage: make docker-compose-black project=<project-name>"
	@echo "Usage: make docker-compose-run project=<project-name>"
	@echo ""
	@echo "Available projects:"
	@echo "  worker  : Starts the Docker containers for the worker."
	@echo "  openadr: Starts the Docker containers for the openadr: ven and ven."
	@echo ""


.PHONY: docker-compose-up
docker-compose-up:
	docker-compose -f docker-compose.$(project).yml up


.PHONY: docker-compose-build
docker-compose-build:
	docker-compose -f docker-compose.$(project).yml build


.PHONY: docker-compose-test
docker-compose-test:
	docker-compose -f docker-compose.$(project).yml run $(project) pytest

.PHONY: docker-compose-black
docker-compose-black:
	docker-compose -f docker-compose.$(project).yml run $(project) black .

.PHONY: docker-compose-test
docker-compose-run:
	docker-compose -f docker-compose.$(project).yml run $(project)

