{
    "paths": {
        "/db/devices/query": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "timeoutInMillis": "${timeoutInMillis}",
                    "connectionType": "INTERNET"
                },
                "summary": "Query devices from gsi",
                "description": "Query devices from devices table with gsi or lsi",
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
                                                "required": [
                                                    "device_id",
                                                    "agent_id",
                                                    "device_type",
                                                    "device_model",
                                                    "flexible",
                                                    "status",
                                                    "valid_at"
                                                ],
                                                "properties": {
                                                    "device_id": {
                                                        "type": "string"
                                                    },
                                                    "agent_id": {
                                                        "type": "string"
                                                    },
                                                    "device_type": {
                                                        "type": "string"
                                                    },
                                                    "device_model": {
                                                        "type": "string"
                                                    },
                                                    "flexible": {
                                                        "type": "integer"
                                                    },
                                                    "status": {
                                                        "type": "integer"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                }
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
        "/db/devices/scan": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "scan devices",
                "description": "Scan items from devices table",
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
                                                "required": [
                                                    "device_id",
                                                    "agent_id",
                                                    "device_type",
                                                    "device_model",
                                                    "flexible",
                                                    "status",
                                                    "valid_at"
                                                ],
                                                "properties": {
                                                    "device_id": {
                                                        "type": "string"
                                                    },
                                                    "agent_id": {
                                                        "type": "string"
                                                    },
                                                    "device_type": {
                                                        "type": "string"
                                                    },
                                                    "device_model": {
                                                        "type": "string"
                                                    },
                                                    "flexible": {
                                                        "type": "integer"
                                                    },
                                                    "status": {
                                                        "type": "integer"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                }
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
        "/db/devices": {
            "post": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Create devices",
                "description": "Create new devices with the given data",
                "requestBody": {
                    "description": "Data for creating new devices",
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
                                            "required": [
                                                "device_id",
                                                "agent_id",
                                                "device_type",
                                                "device_model",
                                                "flexible",
                                                "status",
                                                "valid_at"
                                            ],
                                            "properties": {
                                                "device_id": {
                                                    "type": "string"
                                                },
                                                "agent_id": {
                                                    "type": "string"
                                                },
                                                "device_type": {
                                                    "type": "string"
                                                },
                                                "device_model": {
                                                    "type": "string"
                                                },
                                                "flexible": {
                                                    "type": "integer"
                                                },
                                                "status": {
                                                    "type": "integer"
                                                },
                                                "valid_at": {
                                                    "type": "integer"
                                                }
                                            }
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
                                                "required": [
                                                    "device_id",
                                                    "agent_id",
                                                    "device_type",
                                                    "device_model",
                                                    "flexible",
                                                    "status",
                                                    "valid_at"
                                                ],
                                                "properties": {
                                                    "device_id": {
                                                        "type": "string"
                                                    },
                                                    "agent_id": {
                                                        "type": "string"
                                                    },
                                                    "device_type": {
                                                        "type": "string"
                                                    },
                                                    "device_model": {
                                                        "type": "string"
                                                    },
                                                    "flexible": {
                                                        "type": "integer"
                                                    },
                                                    "status": {
                                                        "type": "integer"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                }
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
                "summary": "Delete devices",
                "description": "Delete new devices with the given data",
                "requestBody": {
                    "description": "Data for deleting devices",
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
                                                    "type": "string",
                                                    "description": "The device ID of the device"
                                                }
                                            },
                                            "required": [
                                                "device_id"
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
        "/db/device/{device_id}": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Get device by ID",
                "description": "Retrieve the device with the specified ID",
                "parameters": [
                    {
                        "name": "device_id",
                        "in": "path",
                        "description": "The ID of the device to retrieve",
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
                                    "required": [
                                        "device_id",
                                        "agent_id",
                                        "device_type",
                                        "device_model",
                                        "flexible",
                                        "status",
                                        "valid_at"
                                    ],
                                    "properties": {
                                        "device_id": {
                                            "type": "string"
                                        },
                                        "agent_id": {
                                            "type": "string"
                                        },
                                        "device_type": {
                                            "type": "string"
                                        },
                                        "device_model": {
                                            "type": "string"
                                        },
                                        "flexible": {
                                            "type": "integer"
                                        },
                                        "status": {
                                            "type": "integer"
                                        },
                                        "valid_at": {
                                            "type": "integer"
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
            "put": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Update an device by device_id",
                "description": "Updae an device with device_id ",
                "parameters": [
                    {
                        "name": "device_id",
                        "in": "path",
                        "description": "The ID of the device to retrieve",
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
                                "required": [
                                    "device_id",
                                    "agent_id",
                                    "device_type",
                                    "device_model",
                                    "flexible",
                                    "status",
                                    "valid_at"
                                ],
                                "properties": {
                                    "device_id": {
                                        "type": "string"
                                    },
                                    "agent_id": {
                                        "type": "string"
                                    },
                                    "device_type": {
                                        "type": "string"
                                    },
                                    "device_model": {
                                        "type": "string"
                                    },
                                    "flexible": {
                                        "type": "integer"
                                    },
                                    "status": {
                                        "type": "integer"
                                    },
                                    "valid_at": {
                                        "type": "integer"
                                    }
                                }
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
                "summary": "Delete an device by device_id",
                "description": "Delete an device with device_id ",
                "parameters": [
                    {
                        "name": "device_id",
                        "in": "path",
                        "description": "The ID of the device to retrieve",
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
        "/db/device": {
            "post": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Create an device by device_id",
                "description": "Create an device ",
                "requestBody": {
                    "description": "Auction resource status update",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": [
                                    "agent_id",
                                    "device_type",
                                    "device_model",
                                    "flexible",
                                    "status"
                                ],
                                "properties": {
                                    "agent_id": {
                                        "type": "string"
                                    },
                                    "device_type": {
                                        "type": "string"
                                    },
                                    "device_model": {
                                        "type": "string"
                                    },
                                    "flexible": {
                                        "type": "integer"
                                    },
                                    "status": {
                                        "type": "integer"
                                    }
                                }
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
                                    "required": [
                                        "device_id",
                                        "agent_id",
                                        "device_type",
                                        "device_model",
                                        "flexible",
                                        "status",
                                        "valid_at"
                                    ],
                                    "properties": {
                                        "device_id": {
                                            "type": "string"
                                        },
                                        "agent_id": {
                                            "type": "string"
                                        },
                                        "device_type": {
                                            "type": "string"
                                        },
                                        "device_model": {
                                            "type": "string"
                                        },
                                        "flexible": {
                                            "type": "integer"
                                        },
                                        "status": {
                                            "type": "integer"
                                        },
                                        "valid_at": {
                                            "type": "integer"
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
        }
    }
}