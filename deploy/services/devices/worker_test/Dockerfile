FROM hashicorp/terraform:1.3.6
LABEL maintainer="Jimmy"

# ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
COPY requirements.dev.txt /tmp/requirements.dev.txt
COPY . /infra
# RUN apk add --no-cache --virtual .build-deps \

RUN apk add --no-cache curl \
        unzip \
        libffi-dev \
    && apk add --no-cache python3-dev \
    && python3 -m ensurepip \
    && python3 -m pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt 
    # && if [ "$DEV" = "true" ]; then \
    #        pip install -r /tmp/requirements.dev.txt; \
    #    fi\
    # && rm -rf /tmp 
    # && adduser \
    #     --disabled-password \
    #     --no-create-home \
    #     openadr-user 
    # && apk del .build-deps
# COPY . /infra
# #     && python3 -m venv /py \
# #     && /py/bin/pip install -r /tmp/requirements.txt \
# #     && if [ "$DEV" = "true" ]; then \
# #            /py/bin/pip install -r /tmp/requirements.dev.txt; \
# #        fi \
# #     && rm -rf /tmp \
# #     # && adduser \
# #     #     --disabled-password \
# #     #     --no-create-home \
# #     #     openadr-user \
# #     && apk del .build-deps



# WORKDIR /infra

# # ENV PATH="/py/bin:$PATH"



ENTRYPOINT ["python", "app.py"]