{
    "paths": {
        "/db/settings/query": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "timeoutInMillis": "${timeoutInMillis}",
                    "connectionType": "INTERNET"
                },
                "summary": "Query settings from gsi",
                "description": "Query settings from settings table with gsi or lsi",
                "parameters": [
                    {
                        "name": "gsi_name",
                        "required": true,
                        "description": "The name of the global secondary index to use (required for query action).",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "key_value",
                        "required": true,
                        "description": "The value of the key to use for the query or scan.",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "key_name",
                        "required": true,
                        "description": "The name of the key to use for the query or scan.",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "key_type",
                        "required": false,
                        "description": "The type of the key to use for the query or scan (string or number, default is string).",
                        "schema": {
                            "type": "string",
                            "enum": [
                                "S",
                                "N"
                            ]
                        }
                    },
                    {
                        "name": "range_key",
                        "required": false,
                        "description": "The name of the range key to use for the query (required for query action).",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "range_key_value",
                        "required": false,
                        "description": "The value of the range key to use for the query.",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "start_from",
                        "required": false,
                        "description": "The timestamp to start querying from (required for query action).",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "end_at",
                        "required": false,
                        "description": "The timestamp to end querying at (required for query action).",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": [
                                        "data"
                                    ],
                                    "properties": {
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "setting_id": {
                                                        "type": "string"
                                                    },
                                                    "device_id": {
                                                        "type": "integer"
                                                    },
                                                    "name": {
                                                        "type": "string"
                                                    },
                                                    "value": {
                                                        "type": "string"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "setting_id",
                                                    "device_id",
                                                    "name",
                                                    "value",
                                                    "valid_at"
                                                ]
                                            }
                                        }
                                    }
                                }
                            }
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
        },
        "/db/settings/scan": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "scan settings",
                "description": "Scan items from settings table",
                "parameters": [
                    {
                        "name": "key_value",
                        "required": true,
                        "description": "The value of the key to use for the query or scan.",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "key_name",
                        "required": true,
                        "description": "The name of the key to use for the query or scan.",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "key_type",
                        "required": false,
                        "description": "The type of the key to use for the query or scan (string or number, default is string).",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": [
                                        "data"
                                    ],
                                    "properties": {
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "setting_id": {
                                                        "type": "string"
                                                    },
                                                    "device_id": {
                                                        "type": "integer"
                                                    },
                                                    "name": {
                                                        "type": "string"
                                                    },
                                                    "value": {
                                                        "type": "string"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "setting_id",
                                                    "device_id",
                                                    "name",
                                                    "value",
                                                    "valid_at"
                                                ]
                                            }
                                        }
                                    }
                                }
                            }
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
        },
        "/db/settings": {
            "post": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Create settings",
                "description": "Create new settings with the given data",
                "requestBody": {
                    "description": "Data for creating new settings",
                    "required": true,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "data": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "device_id": {
                                                    "type": "integer"
                                                },
                                                "name": {
                                                    "type": "string"
                                                },
                                                "value": {
                                                    "type": "string"
                                                }
                                            },
                                            "required": [
                                                "device_id",
                                                "name",
                                                "value"
                                            ]
                                        }
                                    }
                                },
                                "required": [
                                    "data"
                                ]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Auctions created successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "setting_id": {
                                                        "type": "string"
                                                    },
                                                    "device_id": {
                                                        "type": "integer"
                                                    },
                                                    "name": {
                                                        "type": "string"
                                                    },
                                                    "value": {
                                                        "type": "string"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "setting_id",
                                                    "device_id",
                                                    "name",
                                                    "value",
                                                    "valid_at"
                                                ]
                                            }
                                        }
                                    },
                                    "required": [
                                        "data"
                                    ]
                                }
                            }
                        }
                    }
                }
            },
            "delete": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Delete settings",
                "description": "Delete new settings with the given data",
                "requestBody": {
                    "description": "Data for deleting settings",
                    "required": true,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "data": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "setting_id": {
                                                    "type": "string",
                                                    "description": "The setting ID of the setting"
                                                }
                                            },
                                            "required": [
                                                "setting_id"
                                            ]
                                        }
                                    }
                                },
                                "required": [
                                    "data"
                                ]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Auction retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {
                                            "type": "string",
                                            "enum": [
                                                "success"
                                            ]
                                        }
                                    }
                                }
                            }
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
        },
        "/db/setting/{setting_id}": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Get setting by ID",
                "description": "Retrieve the setting with the specified ID",
                "parameters": [
                    {
                        "name": "setting_id",
                        "in": "path",
                        "description": "The ID of the setting to retrieve",
                        "required": true,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Auction retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "setting_id": {
                                            "type": "string"
                                        },
                                        "device_id": {
                                            "type": "integer"
                                        },
                                        "name": {
                                            "type": "string"
                                        },
                                        "value": {
                                            "type": "string"
                                        },
                                        "valid_at": {
                                            "type": "integer"
                                        }
                                    },
                                    "required": [
                                        "setting_id",
                                        "device_id",
                                        "name",
                                        "value",
                                        "valid_at"
                                    ]
                                }
                            }
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
            },
            "put": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Update an setting by setting_id",
                "description": "Updae an setting with setting_id ",
                "parameters": [
                    {
                        "name": "setting_id",
                        "in": "path",
                        "description": "The ID of the setting to retrieve",
                        "required": true,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "requestBody": {
                    "description": "Resource status update",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "setting_id": {
                                        "type": "string"
                                    },
                                    "device_id": {
                                        "type": "integer"
                                    },
                                    "name": {
                                        "type": "string"
                                    },
                                    "value": {
                                        "type": "string"
                                    },
                                    "valid_at": {
                                        "type": "integer"
                                    }
                                },
                                "required": [
                                    "setting_id",
                                    "device_id",
                                    "name",
                                    "value",
                                    "valid_at"
                                ]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Auction retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {
                                            "type": "string",
                                            "enum": [
                                                "success"
                                            ]
                                        }
                                    }
                                }
                            }
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
            },
            "delete": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Delete an setting by setting_id",
                "description": "Delete an setting with setting_id ",
                "parameters": [
                    {
                        "name": "setting_id",
                        "in": "path",
                        "description": "The ID of the setting to retrieve",
                        "required": true,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Auction retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {
                                            "type": "string",
                                            "enum": [
                                                "success"
                                            ]
                                        }
                                    }
                                }
                            }
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
        },
        "/db/setting": {
            "post": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Create an setting by setting_id",
                "description": "Create an setting ",
                "requestBody": {
                    "description": "Auction setting status update",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "device_id": {
                                        "type": "integer"
                                    },
                                    "name": {
                                        "type": "string"
                                    },
                                    "value": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "device_id",
                                    "name",
                                    "value"
                                ]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Auction retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "setting_id": {
                                            "type": "string"
                                        },
                                        "device_id": {
                                            "type": "integer"
                                        },
                                        "name": {
                                            "type": "string"
                                        },
                                        "value": {
                                            "type": "string"
                                        },
                                        "valid_at": {
                                            "type": "integer"
                                        }
                                    },
                                    "required": [
                                        "setting_id",
                                        "device_id",
                                        "name",
                                        "value",
                                        "valid_at"
                                    ]
                                }
                            }
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