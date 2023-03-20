
FROM python:3.9-alpine

LABEL maintainer="Jimmy"

ENV PYTHONUNBUFFERED 1
ENV TERRAFORM_VERSION="1.3.6"

COPY requirements.txt /tmp/requirements.txt
COPY requirements.dev.txt /tmp/requirements.dev.txt

RUN apk add --no-cache --virtual .build-deps \
        curl \
        unzip \
        libffi-dev \
    && python -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && /py/bin/pip install -r /tmp/requirements.txt \
    && if [ "$DEV" = "true" ]; then \
           /py/bin/pip install -r /tmp/requirements.dev.txt; \
       fi \
    && rm -rf /tmp \
    && adduser \
        --disabled-password \
        --no-create-home \
        openadr-user \
    && apk del .build-deps

COPY . /app
WORKDIR /app

ENV PATH="/py/bin:$PATH"


# FROM python:3.9
# LABEL maintainer="Jimmy"

# ENV PYTHONUNBUFFERED 1

# COPY ./requirements.txt /tmp/requirements.txt
# COPY ./requirements.dev.txt /tmp/requirements.dev.txt



# ARG DEV=true
# RUN python -m venv /py && \
#     /py/bin/pip install --upgrade pip  
# RUN apt-get update && \
#     apt-get upgrade -y && \
#     apt-get install -y nodejs build-essential curl locales libffi-dev netcat

# RUN /py/bin/pip install -r /tmp/requirements.txt 

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


# ENV PATH="/py/bin:$PATH"
# CMD [ "python ven.py" ]
