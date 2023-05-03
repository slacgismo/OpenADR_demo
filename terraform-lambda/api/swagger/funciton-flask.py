import boto3
import os
import io
import json
from botocore.exceptions import ClientError
from flask import Flask, redirect, url_for
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

S3_BUCKET = os.environ.get('S3_BUCKET', None)
OPENAPI_KEY = os.environ.get('OPENAPI_KEY', None)

s3 = boto3.client('s3')

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Swagger UI"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


def get_object_body(bucket_name, key):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        body = response['Body'].read()
        return body
    except ClientError as e:
        print(e)
        return None


def get_openapi():
    return json.loads(get_object_body(S3_BUCKET, OPENAPI_KEY))


@app.route('/')
def index():
    return redirect(url_for('swaggerui.index'))


@app.route(API_URL)
def swagger_api():
    return get_openapi()


def handler(event, context):
    response = app.make_response('')
    response.headers.set('Content-Type', 'text/html')
    response.status_code = 200
    response.data = b''

    with app.test_request_context(event['path'], headers=event['headers']):
        response = app.full_dispatch_request()

    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.data.decode('utf-8')
    }
