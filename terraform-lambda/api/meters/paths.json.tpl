{
    "paths": {
        "/db/meters/query": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "timeoutInMillis": "${timeoutInMillis}",
                    "connectionType": "INTERNET"
                },
                "summary": "Query meters from gsi",
                "description": "Query meters from meters table with gsi or lsi",
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
                                                    "meter_id": {
                                                        "type": "string"
                                                    },
                                                    "device_id": {
                                                        "type": "string"
                                                    },
                                                    "resource_id": {
                                                        "type": "string"
                                                    },
                                                    "status": {
                                                        "type": "integer"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "meter_id",
                                                    "device_id",
                                                    "resource_id",
                                                    "status",
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
        "/db/meters/scan": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "scan meters",
                "description": "Scan items from meters table",
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
                                                    "meter_id": {
                                                        "type": "string"
                                                    },
                                                    "device_id": {
                                                        "type": "string"
                                                    },
                                                    "resource_id": {
                                                        "type": "string"
                                                    },
                                                    "status": {
                                                        "type": "integer"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "meter_id",
                                                    "device_id",
                                                    "resource_id",
                                                    "status",
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
        "/db/meters": {
            "post": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Create meters",
                "description": "Create new meters with the given data",
                "requestBody": {
                    "description": "Data for creating new meters",
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
                                                    "type": "string"
                                                },
                                                "resource_id": {
                                                    "type": "string"
                                                },
                                                "status": {
                                                    "type": "integer"
                                                }
                                            },
                                            "required": [
                                                "device_id",
                                                "resource_id",
                                                "status"
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
                                                    "meter_id": {
                                                        "type": "string"
                                                    },
                                                    "device_id": {
                                                        "type": "string"
                                                    },
                                                    "resource_id": {
                                                        "type": "string"
                                                    },
                                                    "status": {
                                                        "type": "integer"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "meter_id",
                                                    "device_id",
                                                    "resource_id",
                                                    "status",
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
                "summary": "Delete meters",
                "description": "Delete new meters with the given data",
                "requestBody": {
                    "description": "Data for deleting meters",
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
                                                "meter_id": {
                                                    "type": "string",
                                                    "description": "The meter ID of the meter"
                                                }
                                            },
                                            "required": [
                                                "meter_id"
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
        "/db/meter/{meter_id}": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Get meter by ID",
                "description": "Retrieve the meter with the specified ID",
                "parameters": [
                    {
                        "name": "meter_id",
                        "in": "path",
                        "description": "The ID of the meter to retrieve",
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
                                        "meter_id": {
                                            "type": "string"
                                        },
                                        "device_id": {
                                            "type": "string"
                                        },
                                        "resource_id": {
                                            "type": "string"
                                        },
                                        "status": {
                                            "type": "integer"
                                        },
                                        "valid_at": {
                                            "type": "integer"
                                        }
                                    },
                                    "required": [
                                        "meter_id",
                                        "device_id",
                                        "resource_id",
                                        "status",
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
                "summary": "Update an meter by meter_id",
                "description": "Updae an meter with meter_id ",
                "parameters": [
                    {
                        "name": "meter_id",
                        "in": "path",
                        "description": "The ID of the meter to retrieve",
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
                                    "meter_id": {
                                        "type": "string"
                                    },
                                    "device_id": {
                                        "type": "string"
                                    },
                                    "resource_id": {
                                        "type": "string"
                                    },
                                    "status": {
                                        "type": "integer"
                                    },
                                    "valid_at": {
                                        "type": "integer"
                                    }
                                },
                                "required": [
                                    "meter_id",
                                    "device_id",
                                    "resource_id",
                                    "status",
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
                "summary": "Delete an meter by meter_id",
                "description": "Delete an meter with meter_id ",
                "parameters": [
                    {
                        "name": "meter_id",
                        "in": "path",
                        "description": "The ID of the meter to retrieve",
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
        "/db/meter": {
            "post": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Create an meter by meter_id",
                "description": "Create an meter ",
                "requestBody": {
                    "description": "Auction resource status update",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "device_id": {
                                        "type": "string"
                                    },
                                    "resource_id": {
                                        "type": "string"
                                    },
                                    "status": {
                                        "type": "integer"
                                    }
                                },
                                "required": [
                                    "device_id",
                                    "resource_id",
                                    "status"
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
                                        "meter_id": {
                                            "type": "string"
                                        },
                                        "device_id": {
                                            "type": "string"
                                        },
                                        "resource_id": {
                                            "type": "string"
                                        },
                                        "status": {
                                            "type": "integer"
                                        },
                                        "valid_at": {
                                            "type": "integer"
                                        }
                                    },
                                    "required": [
                                        "meter_id",
                                        "device_id",
                                        "resource_id",
                                        "status",
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