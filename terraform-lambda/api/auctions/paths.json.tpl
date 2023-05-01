{
    "paths": {
        "/db/auctions/query": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "timeoutInMillis": "${timeoutInMillis}",
                    "connectionType": "INTERNET"
                },
                "summary": "Query auctions from gsi",
                "description": "Query auctions from auctions table with gsi or lsi",
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
                                                    "auction_id",
                                                    "resource_id",
                                                    "status",
                                                    "valid_at"
                                                ],
                                                "properties": {
                                                    "auction_id": {
                                                        "type": "string"
                                                    },
                                                    "market_id": {
                                                        "type": "string"
                                                    },
                                                    "clearing_time": {
                                                        "type": "integer"
                                                    },
                                                    "expected_price": {
                                                        "type": "float"
                                                    },
                                                    "expected_stdev": {
                                                        "type": "float"
                                                    },
                                                    "reference_price": {
                                                        "type": "float"
                                                    },
                                                    "price": {
                                                        "type": "float"
                                                    },
                                                    "quantity": {
                                                        "type": "float"
                                                    },
                                                    "marginal_type": {
                                                        "type": "string"
                                                    },
                                                    "marginal_order": {
                                                        "type": "string"
                                                    },
                                                    "marginal_quantity": {
                                                        "type": "float"
                                                    },
                                                    "marginal_rank": {
                                                        "type": "string"
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
        "/db/auctions/scan": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "scan auctions",
                "description": "Scan items from auctions table",
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
                                                    "auction_id",
                                                    "resource_id",
                                                    "status",
                                                    "valid_at"
                                                ],
                                                "properties": {
                                                    "auction_id": {
                                                        "type": "string"
                                                    },
                                                    "market_id": {
                                                        "type": "string"
                                                    },
                                                    "clearing_time": {
                                                        "type": "integer"
                                                    },
                                                    "expected_price": {
                                                        "type": "float"
                                                    },
                                                    "expected_stdev": {
                                                        "type": "float"
                                                    },
                                                    "reference_price": {
                                                        "type": "float"
                                                    },
                                                    "price": {
                                                        "type": "float"
                                                    },
                                                    "quantity": {
                                                        "type": "float"
                                                    },
                                                    "marginal_type": {
                                                        "type": "string"
                                                    },
                                                    "marginal_order": {
                                                        "type": "string"
                                                    },
                                                    "marginal_quantity": {
                                                        "type": "float"
                                                    },
                                                    "marginal_rank": {
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
        "/db/auctions": {
            "post": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Create auctions",
                "description": "Create new auctions with the given data",
                "requestBody": {
                    "description": "Data for creating new auctions",
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
                                                "market_id": {
                                                    "type": "string"
                                                },
                                                "clearing_time": {
                                                    "type": "integer"
                                                },
                                                "expected_price": {
                                                    "type": "float"
                                                },
                                                "expected_stdev": {
                                                    "type": "float"
                                                },
                                                "reference_price": {
                                                    "type": "float"
                                                },
                                                "price": {
                                                    "type": "float"
                                                },
                                                "quantity": {
                                                    "type": "float"
                                                },
                                                "marginal_type": {
                                                    "type": "string"
                                                },
                                                "marginal_order": {
                                                    "type": "string"
                                                },
                                                "marginal_quantity": {
                                                    "type": "float"
                                                },
                                                "marginal_rank": {
                                                    "type": "string"
                                                }
                                            },
                                            "required": [
                                                "market_id",
                                                "clearing_time",
                                                "expected_price",
                                                "expected_stdev",
                                                "reference_price",
                                                "price",
                                                "quantity",
                                                "marginal_type",
                                                "marginal_order",
                                                "marginal_quantity",
                                                "marginal_rank"
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
                                                    "auction_id": {
                                                        "type": "string"
                                                    }
                                            
                                                },
                                                "required": [
                                                    "auction_id"
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
                "summary": "Delete auctions",
                "description": "Delete new auctions with the given data",
                "requestBody": {
                    "description": "Data for deleting auctions",
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
                                                "auction_id": {
                                                    "type": "string",
                                                    "description": "The auction ID of the auction"
                                                }
                                            },
                                            "required": [
                                                "auction_id"
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
        "/db/auction/{auction_id}": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Get auction by ID",
                "description": "Retrieve the auction with the specified ID",
                "parameters": [
                    {
                        "name": "auction_id",
                        "in": "path",
                        "description": "The ID of the auction to retrieve",
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
                                        "auction_id": {
                                            "type": "string"
                                        },
                                        "market_id": {
                                            "type": "string"
                                        },
                                        "clearing_time": {
                                            "type": "integer"
                                        },
                                        "expected_price": {
                                            "type": "float"
                                        },
                                        "expected_stdev": {
                                            "type": "float"
                                        },
                                        "reference_price": {
                                            "type": "float"
                                        },
                                        "price": {
                                            "type": "float"
                                        },
                                        "quantity": {
                                            "type": "float"
                                        },
                                        "marginal_type": {
                                            "type": "string"
                                        },
                                        "marginal_order": {
                                            "type": "string"
                                        },
                                        "marginal_quantity": {
                                            "type": "float"
                                        },
                                        "marginal_rank": {
                                            "type": "string"
                                        }
                                    },
                                    "required": [
                                        "auction_id",
                                        "market_id",
                                        "clearing_time",
                                        "expected_price",
                                        "expected_stdev",
                                        "reference_price",
                                        "price",
                                        "quantity",
                                        "marginal_type",
                                        "marginal_order",
                                        "marginal_quantity",
                                        "marginal_rank"
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
                "summary": "Update an auction by auction_id",
                "description": "Updae an auction with auction_id ",
                "parameters": [
                    {
                        "name": "auction_id",
                        "in": "path",
                        "description": "The ID of the auction to retrieve",
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
                                    "market_id": {
                                        "type": "string"
                                    },
                                    "clearing_time": {
                                        "type": "integer"
                                    },
                                    "expected_price": {
                                        "type": "float"
                                    },
                                    "expected_stdev": {
                                        "type": "float"
                                    },
                                    "reference_price": {
                                        "type": "float"
                                    },
                                    "price": {
                                        "type": "float"
                                    },
                                    "quantity": {
                                        "type": "float"
                                    },
                                    "marginal_type": {
                                        "type": "string"
                                    },
                                    "marginal_order": {
                                        "type": "string"
                                    },
                                    "marginal_quantity": {
                                        "type": "float"
                                    },
                                    "marginal_rank": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "market_id",
                                    "clearing_time",
                                    "expected_price",
                                    "expected_stdev",
                                    "reference_price",
                                    "price",
                                    "quantity",
                                    "marginal_type",
                                    "marginal_order",
                                    "marginal_quantity",
                                    "marginal_rank"
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
                "summary": "Delete an auction by auction_id",
                "description": "Delete an auction with auction_id ",
                "parameters": [
                    {
                        "name": "auction_id",
                        "in": "path",
                        "description": "The ID of the auction to retrieve",
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
        "/db/auction": {
            "post": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Create an auction by auction_id",
                "description": "Create an auction ",
                "requestBody": {
                    "description": "Auction resource status update",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "market_id": {
                                        "type": "string"
                                    },
                                    "clearing_time": {
                                        "type": "integer"
                                    },
                                    "expected_price": {
                                        "type": "float"
                                    },
                                    "expected_stdev": {
                                        "type": "float"
                                    },
                                    "reference_price": {
                                        "type": "float"
                                    },
                                    "price": {
                                        "type": "float"
                                    },
                                    "quantity": {
                                        "type": "float"
                                    },
                                    "marginal_type": {
                                        "type": "string"
                                    },
                                    "marginal_order": {
                                        "type": "string"
                                    },
                                    "marginal_quantity": {
                                        "type": "float"
                                    },
                                    "marginal_rank": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "market_id",
                                    "clearing_time",
                                    "expected_price",
                                    "expected_stdev",
                                    "reference_price",
                                    "price",
                                    "quantity",
                                    "marginal_type",
                                    "marginal_order",
                                    "marginal_quantity",
                                    "marginal_rank"
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
                                        "auction_id": {
                                            "type": "string"
                                        }
                                      
                                    },
                                    "required": [
                                        "auction_id"
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