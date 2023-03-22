FROM hashicorp/terraform:1.3.6
LABEL maintainer="Jimmy"

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
COPY requirements.dev.txt /tmp/requirements.dev.txt

RUN apk add --no-cache --virtual .build-deps \
        curl \
        unzip \
        libffi-dev \
    && apk add --no-cache python3-dev \
    && python3 -m ensurepip \
    && python3 -m pip install --upgrade pip \
    && python3 -m venv /py \
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

ENTRYPOINT ["python", "app.py"]