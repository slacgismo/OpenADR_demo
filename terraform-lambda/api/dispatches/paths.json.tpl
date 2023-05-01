{
    "paths": {
        "/db/dispatches/query": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "timeoutInMillis": "${timeoutInMillis}",
                    "connectionType": "INTERNET"
                },
                "summary": "Query dispatches from gsi",
                "description": "Query dispatches from dispatches table with gsi or lsi",
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
                                                    "order_id": {
                                                        "type": "string"
                                                    },
                                                    "record_time": {
                                                        "type": "integer"
                                                    },
                                                    "quantity": {
                                                        "type": "float"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "order_id",
                                                    "record_time",
                                                    "quantity",
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
        "/db/dispatches/scan": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "scan dispatches",
                "description": "Scan items from dispatches table",
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
                                                    "order_id": {
                                                        "type": "string"
                                                    },
                                                    "record_time": {
                                                        "type": "integer"
                                                    },
                                                    "quantity": {
                                                        "type": "float"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "order_id",
                                                    "record_time",
                                                    "quantity",
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
        "/db/dispatches": {
            "post": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Create dispatches",
                "description": "Create new dispatches with the given data",
                "requestBody": {
                    "description": "Data for creating new dispatches",
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
                                                "record_time": {
                                                    "type": "integer"
                                                },
                                                "quantity": {
                                                    "type": "float"
                                                }
                                            },
                                            "required": [
                                                "record_time",
                                                "quantity"
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
                                                    "order_id": {
                                                        "type": "string"
                                                    },
                                                    "record_time": {
                                                        "type": "integer"
                                                    },
                                                    "quantity": {
                                                        "type": "float"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "order_id",
                                                    "record_time",
                                                    "quantity",
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
                "summary": "Delete dispatches",
                "description": "Delete new dispatches with the given data",
                "requestBody": {
                    "description": "Data for deleting dispatches",
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
                                                "dispatch_id": {
                                                    "type": "string",
                                                    "description": "The dispatch ID of the dispatch"
                                                }
                                            },
                                            "required": [
                                                "dispatch_id"
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
        "/db/dispatch/{dispatch_id}": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Get dispatch by ID",
                "description": "Retrieve the dispatch with the specified ID",
                "parameters": [
                    {
                        "name": "dispatch_id",
                        "in": "path",
                        "description": "The ID of the dispatch to retrieve",
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
                                        "order_id": {
                                            "type": "string"
                                        },
                                        "record_time": {
                                            "type": "integer"
                                        },
                                        "quantity": {
                                            "type": "float"
                                        },
                                        "valid_at": {
                                            "type": "integer"
                                        }
                                    },
                                    "required": [
                                        "order_id",
                                        "record_time",
                                        "quantity",
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
                "summary": "Update an dispatch by dispatch_id",
                "description": "Updae an dispatch with dispatch_id ",
                "parameters": [
                    {
                        "name": "dispatch_id",
                        "in": "path",
                        "description": "The ID of the dispatch to retrieve",
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
                                    "order_id": {
                                        "type": "string"
                                    },
                                    "record_time": {
                                        "type": "integer"
                                    },
                                    "quantity": {
                                        "type": "float"
                                    },
                                    "valid_at": {
                                        "type": "integer"
                                    }
                                },
                                "required": [
                                    "order_id",
                                    "record_time",
                                    "quantity",
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
                "summary": "Delete an dispatch by dispatch_id",
                "description": "Delete an dispatch with dispatch_id ",
                "parameters": [
                    {
                        "name": "dispatch_id",
                        "in": "path",
                        "description": "The ID of the dispatch to retrieve",
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
        "/db/dispatch": {
            "post": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Create an dispatch by dispatch_id",
                "description": "Create an dispatch ",
                "requestBody": {
                    "description": "Auction resource status update",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "record_time": {
                                        "type": "integer"
                                    },
                                    "quantity": {
                                        "type": "float"
                                    }
                                },
                                "required": [
                                    "record_time",
                                    "quantity"
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
                                        "order_id": {
                                            "type": "string"
                                        },
                                        "record_time": {
                                            "type": "integer"
                                        },
                                        "quantity": {
                                            "type": "float"
                                        },
                                        "valid_at": {
                                            "type": "integer"
                                        }
                                    },
                                    "required": [
                                        "order_id",
                                        "record_time",
                                        "quantity",
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