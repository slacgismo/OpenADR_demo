FROM python:3.9-slim-buster

LABEL maintainer="Jimmy"
ENV DEV="true"
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
COPY requirements.dev.txt /tmp/requirements.dev.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        unzip \
        libffi-dev \
    && python -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && /py/bin/pip install -r /tmp/requirements.txt \
    && if [ "$DEV" = "true" ]; then \
           /py/bin/pip install -r /tmp/requirements.dev.txt; \
       fi \
    && adduser \
        --disabled-password \
        --no-create-home \
        openadr-user \
    && apt-get remove -y --auto-remove \
        curl \
        unzip \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

ENV PATH="/py/bin:$PATH"

# FROM python:3.9-slim-buster

# LABEL maintainer="Jimmy"

# ENV PYTHONUNBUFFERED 1
# ENV TERRAFORM_VERSION="1.3.6"

# COPY requirements.txt /tmp/requirements.txt
# COPY requirements.dev.txt /tmp/requirements.dev.txt

# RUN apk add --no-cache --virtual .build-deps \
#         curl \
#         unzip \
#         libffi-dev \
#     && python -m venv /py \
#     && /py/bin/pip install --upgrade pip \
#     && /py/bin/pip install -r /tmp/requirements.txt \
#     && if [ "$DEV" = "true" ]; then \
#            /py/bin/pip install -r /tmp/requirements.dev.txt; \
#        fi \
#     && rm -rf /tmp \
#     && adduser \
#         --disabled-password \
#         --no-create-home \
#         openadr-user \
#     && apk del .build-deps

# COPY . /app
# WORKDIR /app

# ENV PATH="/py/bin:$PATH"

