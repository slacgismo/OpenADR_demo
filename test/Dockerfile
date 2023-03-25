FROM hashicorp/terraform:1.4.2
# Install required packages
RUN apk add --update --no-cache curl docker docker-compose
# Start Docker daemon
RUN dockerd & sleep 5

# Set the working directory to /app
WORKDIR /app

# Copy the Terraform files into the container
COPY . .