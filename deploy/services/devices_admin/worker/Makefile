#####################################################
# Makefile containing shortcut commands for project #
#####################################################


.PHONY: tf-init
tf-init:
	docker-compose -f terraform/docker-compose.yml run --rm terraform init -backend-config=backend.hcl

.PHONY: tf-fmt
tf-fmt:
	docker-compose -f deploy/docker-compose.yml run --rm terraform fmt

.PHONY: tf-validate
tf-validate:
	docker-compose -f deploy/docker-compose.yml run --rm terraform validate 

.PHONY: tf-plan
tf-plan:
	docker-compose -f deploy/docker-compose.yml run --rm terraform plan -backend-config=backend.hcl

.PHONY: tf-apply-auto
tf-apply:
	docker-compose -f deploy/docker-compose.yml run --rm terraform apply --auto-approve