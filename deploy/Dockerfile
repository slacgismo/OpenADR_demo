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

# Set the working directory
WORKDIR /app

# Copy your Terraform code to the container
COPY . .

# Run the Docker daemon
CMD ["dockerd"]

# Expose the Docker daemon
EXPOSE 2375