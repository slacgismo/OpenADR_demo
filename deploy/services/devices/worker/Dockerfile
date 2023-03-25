
FROM python:3.9-alpine

LABEL maintainer="Jimmy"

ENV PYTHONUNBUFFERED 1
ENV TERRAFORM_VERSION="1.4.2"

COPY requirements.txt /tmp/requirements.txt
COPY requirements.dev.txt /tmp/requirements.dev.txt

RUN apk add --no-cache --virtual .build-deps \
        curl \
        unzip \
        libffi-dev \
    && curl https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip > terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
       unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /bin && \
       rm -f terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && python -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && /py/bin/pip install -r /tmp/requirements.txt \
    && if [ "$DEV" = "true" ]; then \
           /py/bin/pip install -r /tmp/requirements.dev.txt; \
       fi \
    # && rm -rf /tmp \
    && adduser \
        --disabled-password \
        --no-create-home \
        openadr-user \
    && apk del .build-deps \
    && apk add --no-cache curl


COPY . /app
WORKDIR /app

ENV PATH="/py/bin:$PATH"

