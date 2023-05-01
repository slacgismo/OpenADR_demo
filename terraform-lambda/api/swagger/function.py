import json
import boto3
import os
import zipfile
import io

from botocore.exceptions import ClientError

s3 = boto3.client('s3')

S3_BUCKET = os.environ.get('S3_BUCKET', None)
OPENAPI_KEY = os.environ.get('OPENAPI_KEY', None)


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


def create_swagger_ui_html():
    openapi = get_openapi()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Swagger UI</title>
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.0.0/swagger-ui.css" />
        <style>
            html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
            *, *:before, *:after { box-sizing: inherit; }
            body { margin:0; background: #fafafa; }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.0.0/swagger-ui-bundle.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.0.0/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {
                const ui = SwaggerUIBundle({
                    spec: """ + json.dumps(openapi) + """,
                    dom_id: '#swagger-ui',
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    layout: "StandaloneLayout"
                })
            }
        </script>
    </body>
    </html>
    """

    return html


def handler(event, context):
    html = create_swagger_ui_html()

    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": html
    }

    return response
