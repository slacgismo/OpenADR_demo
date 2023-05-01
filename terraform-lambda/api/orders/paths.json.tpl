{
    "paths": {
        "/db/orders/query": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "timeoutInMillis": "${timeoutInMillis}",
                    "connectionType": "INTERNET"
                },
                "summary": "Query orders from gsi",
                "description": "Query orders from orders table with gsi or lsi",
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
                                                    "device_id": {
                                                        "type": "string"
                                                    },
                                                    "auction_id": {
                                                        "type": "string"
                                                    },
                                                    "resource_id": {
                                                        "type": "string"
                                                    },
                                                    "record_time": {
                                                        "type": "string"
                                                    },
                                                    "quantity": {
                                                        "type": "float"
                                                    },
                                                    "price": {
                                                        "type": "float"
                                                    },
                                                    "flexible": {
                                                        "type": "integer"
                                                    },
                                                    "state": {
                                                        "type": "float"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "order_id",
                                                    "device_id",
                                                    "auction_id",
                                                    "resource_id",
                                                    "record_time",
                                                    "quantity",
                                                    "price",
                                                    "flexible",
                                                    "state",
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
        "/db/orders/scan": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "scan orders",
                "description": "Scan items from orders table",
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
                                                    "device_id": {
                                                        "type": "string"
                                                    },
                                                    "auction_id": {
                                                        "type": "string"
                                                    },
                                                    "resource_id": {
                                                        "type": "string"
                                                    },
                                                    "record_time": {
                                                        "type": "string"
                                                    },
                                                    "quantity": {
                                                        "type": "float"
                                                    },
                                                    "price": {
                                                        "type": "float"
                                                    },
                                                    "flexible": {
                                                        "type": "integer"
                                                    },
                                                    "state": {
                                                        "type": "float"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "order_id",
                                                    "device_id",
                                                    "auction_id",
                                                    "resource_id",
                                                    "record_time",
                                                    "quantity",
                                                    "price",
                                                    "flexible",
                                                    "state",
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
        "/db/orders": {
            "post": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Create orders",
                "description": "Create new orders with the given data",
                "requestBody": {
                    "description": "Data for creating new orders",
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
                                                "auction_id": {
                                                    "type": "string"
                                                },
                                                "resource_id": {
                                                    "type": "string"
                                                },
                                                "record_time": {
                                                    "type": "string"
                                                },
                                                "quantity": {
                                                    "type": "float"
                                                },
                                                "price": {
                                                    "type": "float"
                                                },
                                                "flexible": {
                                                    "type": "integer"
                                                },
                                                "state": {
                                                    "type": "float"
                                                }
                                            },
                                            "required": [
                                                "device_id",
                                                "auction_id",
                                                "resource_id",
                                                "record_time",
                                                "quantity",
                                                "price",
                                                "flexible",
                                                "state"
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
                                                    "device_id": {
                                                        "type": "string"
                                                    },
                                                    "auction_id": {
                                                        "type": "string"
                                                    },
                                                    "resource_id": {
                                                        "type": "string"
                                                    },
                                                    "record_time": {
                                                        "type": "string"
                                                    },
                                                    "quantity": {
                                                        "type": "float"
                                                    },
                                                    "price": {
                                                        "type": "float"
                                                    },
                                                    "flexible": {
                                                        "type": "integer"
                                                    },
                                                    "state": {
                                                        "type": "float"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "order_id",
                                                    "device_id",
                                                    "auction_id",
                                                    "resource_id",
                                                    "record_time",
                                                    "quantity",
                                                    "price",
                                                    "flexible",
                                                    "state",
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
                "summary": "Delete orders",
                "description": "Delete new orders with the given data",
                "requestBody": {
                    "description": "Data for deleting orders",
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
                                                "order_id": {
                                                    "type": "string",
                                                    "description": "The order ID of the order"
                                                }
                                            },
                                            "required": [
                                                "order_id"
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
        "/db/order/{order_id}": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Get order by ID",
                "description": "Retrieve the order with the specified ID",
                "parameters": [
                    {
                        "name": "order_id",
                        "in": "path",
                        "description": "The ID of the order to retrieve",
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
                                        "device_id": {
                                            "type": "string"
                                        },
                                        "auction_id": {
                                            "type": "string"
                                        },
                                        "resource_id": {
                                            "type": "string"
                                        },
                                        "record_time": {
                                            "type": "string"
                                        },
                                        "quantity": {
                                            "type": "float"
                                        },
                                        "price": {
                                            "type": "float"
                                        },
                                        "flexible": {
                                            "type": "integer"
                                        },
                                        "state": {
                                            "type": "float"
                                        },
                                        "valid_at": {
                                            "type": "integer"
                                        }
                                    },
                                    "required": [
                                        "order_id",
                                        "device_id",
                                        "auction_id",
                                        "resource_id",
                                        "record_time",
                                        "quantity",
                                        "price",
                                        "flexible",
                                        "state",
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
                "summary": "Update an order by order_id",
                "description": "Updae an order with order_id ",
                "parameters": [
                    {
                        "name": "order_id",
                        "in": "path",
                        "description": "The ID of the order to retrieve",
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
                                    "device_id": {
                                        "type": "string"
                                    },
                                    "auction_id": {
                                        "type": "string"
                                    },
                                    "resource_id": {
                                        "type": "string"
                                    },
                                    "record_time": {
                                        "type": "string"
                                    },
                                    "quantity": {
                                        "type": "float"
                                    },
                                    "price": {
                                        "type": "float"
                                    },
                                    "flexible": {
                                        "type": "integer"
                                    },
                                    "state": {
                                        "type": "float"
                                    },
                                    "valid_at": {
                                        "type": "integer"
                                    }
                                },
                                "required": [
                                    "order_id",
                                    "device_id",
                                    "auction_id",
                                    "resource_id",
                                    "record_time",
                                    "quantity",
                                    "price",
                                    "flexible",
                                    "state",
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
                "summary": "Delete an order by order_id",
                "description": "Delete an order with order_id ",
                "parameters": [
                    {
                        "name": "order_id",
                        "in": "path",
                        "description": "The ID of the order to retrieve",
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
        "/db/order": {
            "post": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Create an order by order_id",
                "description": "Create an order ",
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
                                    "auction_id": {
                                        "type": "string"
                                    },
                                    "resource_id": {
                                        "type": "string"
                                    },
                                    "record_time": {
                                        "type": "string"
                                    },
                                    "quantity": {
                                        "type": "float"
                                    },
                                    "price": {
                                        "type": "float"
                                    },
                                    "flexible": {
                                        "type": "integer"
                                    },
                                    "state": {
                                        "type": "float"
                                    }
                                },
                                "required": [
                                    "device_id",
                                    "auction_id",
                                    "resource_id",
                                    "record_time",
                                    "quantity",
                                    "price",
                                    "flexible",
                                    "state"
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
                                        "device_id": {
                                            "type": "string"
                                        },
                                        "auction_id": {
                                            "type": "string"
                                        },
                                        "resource_id": {
                                            "type": "string"
                                        },
                                        "record_time": {
                                            "type": "string"
                                        },
                                        "quantity": {
                                            "type": "float"
                                        },
                                        "price": {
                                            "type": "float"
                                        },
                                        "flexible": {
                                            "type": "integer"
                                        },
                                        "state": {
                                            "type": "float"
                                        },
                                        "valid_at": {
                                            "type": "integer"
                                        }
                                    },
                                    "required": [
                                        "order_id",
                                        "device_id",
                                        "auction_id",
                                        "resource_id",
                                        "record_time",
                                        "quantity",
                                        "price",
                                        "flexible",
                                        "state",
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