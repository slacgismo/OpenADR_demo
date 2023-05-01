{
    "paths": {
        "/db/swagger": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "timeoutInMillis": "${timeoutInMillis}",
                    "connectionType": "INTERNET"
                },
                "summary": "Get swagger UI",
                "description": "Get swagger ui",
                "responses": {
                    "200": {
                        "description": "Failed response",
                        "content": {
                            "application/json": {}
                        }
                    },
                    "400": {
                        "description": "Failed response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "error": {
                                            "type": "string"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}