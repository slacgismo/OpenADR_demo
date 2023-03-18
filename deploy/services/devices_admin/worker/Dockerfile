FROM python:3.9
LABEL maintainer="Jimmy"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt


ENV TERRAFORM_VERSION="1.3.6"

RUN curl https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip > terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
  unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /bin && \
  rm -f terraform_${TERRAFORM_VERSION}_linux_amd64.zip


ARG DEV=true
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip  
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y nodejs build-essential curl locales libffi-dev netcat

RUN /py/bin/pip install -r /tmp/requirements.txt 

RUN if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    # apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        openadr-user

COPY . /app
WORKDIR  /app


ENV PATH="/py/bin:$PATH"
# CMD [ "python ./app/vtn.py" ]


# FROM python:3.9-alpine

# ENV PYTHONUNBUFFERED 1

# COPY ./requirements.txt /tmp/requirements.txt
# COPY ./requirements.dev.txt /tmp/requirements.dev.txt


# RUN apk add --update git bash curl unzip zip openssl make

# ENV TERRAFORM_VERSION="1.3.6"

# RUN curl https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip > terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
#   unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /bin && \
#   rm -f terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# RUN pip install awscli boto3
# RUN python -m venv /py && \
#     /py/bin/pip install --upgrade pip && \
#     /py/bin/pip install -r /tmp/requirements.txt 

# RUN if [ $DEV = "true" ]; \
#         then /py/bin/pip install -r /tmp/requirements.dev.txt; \
#     fi && \
#     rm -rf /tmp && \
#     # apk del .tmp-build-deps && \
#     adduser \
#         --disabled-password \
#         --no-create-home \
#         openadr-user

# COPY . /app
# WORKDIR  /app

