# Use the hashicorp/terraform:1.3.6 as the base image
FROM hashicorp/terraform:1.4.2

# Install required packages
RUN apk add --update --no-cache curl docker docker-compose
# Start Docker daemon

# Copy the Terraform files into the container
COPY . /infra


WORKDIR /infra

