# Use the hashicorp/terraform:1.3.6 as the base image
FROM hashicorp/terraform:1.3.6


# Install dependencies
RUN apk update && \
    apk add --no-cache \
        bash \
        curl \
        docker \
        python3 \
        py3-pip && \
    pip3 install awscli && \
    rm -rf /var/cache/apk/*

# Install Docker Compose
ENV DOCKER_COMPOSE_VERSION 1.29.2
RUN curl --insecure -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose
# Set up Docker daemon to listen on TCP port
RUN mkdir -p /etc/docker && \
    echo '{ "hosts": ["tcp://0.0.0.0:2375", "unix:///var/run/docker.sock"] }' > /etc/docker/daemon.json

# Expose Docker daemon port
EXPOSE 2375

# # Set the working directory
# WORKDIR /app

# # Copy your Terraform code to the container
# COPY . .

# # Run the Docker daemon
# CMD ["dockerd"]

# # Expose the Docker daemon
# EXPOSE 2375

# Set the Docker build arguments
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

# Run the Docker build and push commands
RUN eval $(aws ecr get-login --no-include-email --region $AWS_DEFAULT_REGION) && \
    docker build -t my-image . && \
    docker tag my-image:latest my-repo/my-image:latest && \
    docker push my-repo/my-image:latest