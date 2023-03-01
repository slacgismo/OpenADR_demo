FROM public.ecr.aws/lambda/python:3.8
RUN yum update -y && \
  yum install -y git && \
  rm -Rf /var/cache/yum && \
  pip install git-remote-codecommit boto3 GitPython awscli
COPY index.py ${LAMBDA_TASK_ROOT}
CMD [ "index.handler" ]