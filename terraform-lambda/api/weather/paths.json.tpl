{
    "paths": {
        "/db/weathers/query": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "timeoutInMillis": "${timeoutInMillis}",
                    "connectionType": "INTERNET"
                },
                "summary": "Query weathers from gsi",
                "description": "Query weathers from weathers table with gsi or lsi",
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
                                                    "weather_id": {
                                                        "type": "string"
                                                    },
                                                    "zip_code": {
                                                        "type": "integer"
                                                    },
                                                    "temperature": {
                                                        "type": "float"
                                                    },
                                                    "humidity": {
                                                        "type": "float"
                                                    },
                                                    "solar": {
                                                        "type": "float"
                                                    },
                                                    "wind_speed": {
                                                        "type": "float"
                                                    },
                                                    "wind_direction": {
                                                        "type": "float"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "weather_id",
                                                    "zip_code",
                                                    "temperature",
                                                    "humidity",
                                                    "solar",
                                                    "wind_speed",
                                                    "wind_direction",
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
        "/db/weathers/scan": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "scan weathers",
                "description": "Scan items from weathers table",
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
                                                    "weather_id": {
                                                        "type": "string"
                                                    },
                                                    "zip_code": {
                                                        "type": "integer"
                                                    },
                                                    "temperature": {
                                                        "type": "float"
                                                    },
                                                    "humidity": {
                                                        "type": "float"
                                                    },
                                                    "solar": {
                                                        "type": "float"
                                                    },
                                                    "wind_speed": {
                                                        "type": "float"
                                                    },
                                                    "wind_direction": {
                                                        "type": "float"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "weather_id",
                                                    "zip_code",
                                                    "temperature",
                                                    "humidity",
                                                    "solar",
                                                    "wind_speed",
                                                    "wind_direction",
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
        "/db/weathers": {
            "post": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Create weathers",
                "description": "Create new weathers with the given data",
                "requestBody": {
                    "description": "Data for creating new weathers",
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
                                                "zip_code": {
                                                    "type": "integer"
                                                },
                                                "temperature": {
                                                    "type": "float"
                                                },
                                                "humidity": {
                                                    "type": "float"
                                                },
                                                "solar": {
                                                    "type": "float"
                                                },
                                                "wind_speed": {
                                                    "type": "float"
                                                },
                                                "wind_direction": {
                                                    "type": "float"
                                                }
                                            },
                                            "required": [
                                                "zip_code",
                                                "temperature",
                                                "humidity",
                                                "solar",
                                                "wind_speed",
                                                "wind_direction"
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
                                                    "weather_id": {
                                                        "type": "string"
                                                    },
                                                    "zip_code": {
                                                        "type": "integer"
                                                    },
                                                    "temperature": {
                                                        "type": "float"
                                                    },
                                                    "humidity": {
                                                        "type": "float"
                                                    },
                                                    "solar": {
                                                        "type": "float"
                                                    },
                                                    "wind_speed": {
                                                        "type": "float"
                                                    },
                                                    "wind_direction": {
                                                        "type": "float"
                                                    },
                                                    "valid_at": {
                                                        "type": "integer"
                                                    }
                                                },
                                                "required": [
                                                    "weather_id",
                                                    "zip_code",
                                                    "temperature",
                                                    "humidity",
                                                    "solar",
                                                    "wind_speed",
                                                    "wind_direction",
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
                "summary": "Delete weathers",
                "description": "Delete new weathers with the given data",
                "requestBody": {
                    "description": "Data for deleting weathers",
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
                                                "weather_id": {
                                                    "type": "string",
                                                    "description": "The weather ID of the weather"
                                                }
                                            },
                                            "required": [
                                                "weather_id"
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
        "/db/weather/{weather_id}": {
            "get": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Get weather by ID",
                "description": "Retrieve the weather with the specified ID",
                "parameters": [
                    {
                        "name": "weather_id",
                        "in": "path",
                        "description": "The ID of the weather to retrieve",
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
                                        "weather_id": {
                                            "type": "string"
                                        },
                                        "zip_code": {
                                            "type": "integer"
                                        },
                                        "temperature": {
                                            "type": "float"
                                        },
                                        "humidity": {
                                            "type": "float"
                                        },
                                        "solar": {
                                            "type": "float"
                                        },
                                        "wind_speed": {
                                            "type": "float"
                                        },
                                        "wind_direction": {
                                            "type": "float"
                                        },
                                        "valid_at": {
                                            "type": "integer"
                                        }
                                    },
                                    "required": [
                                        "weather_id",
                                        "zip_code",
                                        "temperature",
                                        "humidity",
                                        "solar",
                                        "wind_speed",
                                        "wind_direction",
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
                "summary": "Update an weather by weather_id",
                "description": "Updae an weather with weather_id ",
                "parameters": [
                    {
                        "name": "weather_id",
                        "in": "path",
                        "description": "The ID of the weather to retrieve",
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
                                    "weather_id": {
                                        "type": "string"
                                    },
                                    "zip_code": {
                                        "type": "integer"
                                    },
                                    "temperature": {
                                        "type": "float"
                                    },
                                    "humidity": {
                                        "type": "float"
                                    },
                                    "solar": {
                                        "type": "float"
                                    },
                                    "wind_speed": {
                                        "type": "float"
                                    },
                                    "wind_direction": {
                                        "type": "float"
                                    },
                                    "valid_at": {
                                        "type": "integer"
                                    }
                                },
                                "required": [
                                    "weather_id",
                                    "zip_code",
                                    "temperature",
                                    "humidity",
                                    "solar",
                                    "wind_speed",
                                    "wind_direction",
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
                "summary": "Delete an weather by weather_id",
                "description": "Delete an weather with weather_id ",
                "parameters": [
                    {
                        "name": "weather_id",
                        "in": "path",
                        "description": "The ID of the weather to retrieve",
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
        "/db/weather": {
            "post": {
                "x-amazon-apigateway-integration": {
                    "payloadFormatVersion": "1.0",
                    "type": "aws_proxy",
                    "httpMethod": "POST",
                    "uri": "${lambda_uri}",
                    "connectionType": "INTERNET",
                    "timeoutInMillis": "${timeoutInMillis}"
                },
                "summary": "Create an weather by weather_id",
                "description": "Create an weather ",
                "requestBody": {
                    "description": "Auction weather status update",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "zip_code": {
                                        "type": "integer"
                                    },
                                    "temperature": {
                                        "type": "float"
                                    },
                                    "humidity": {
                                        "type": "float"
                                    },
                                    "solar": {
                                        "type": "float"
                                    },
                                    "wind_speed": {
                                        "type": "float"
                                    },
                                    "wind_direction": {
                                        "type": "float"
                                    }
                                },
                                "required": [
                                    "zip_code",
                                    "temperature",
                                    "humidity",
                                    "solar",
                                    "wind_speed",
                                    "wind_direction"
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
                                        "weather_id": {
                                            "type": "string"
                                        },
                                        "zip_code": {
                                            "type": "integer"
                                        },
                                        "temperature": {
                                            "type": "float"
                                        },
                                        "humidity": {
                                            "type": "float"
                                        },
                                        "solar": {
                                            "type": "float"
                                        },
                                        "wind_speed": {
                                            "type": "float"
                                        },
                                        "wind_direction": {
                                            "type": "float"
                                        },
                                        "valid_at": {
                                            "type": "integer"
                                        }
                                    },
                                    "required": [
                                        "weather_id",
                                        "zip_code",
                                        "temperature",
                                        "humidity",
                                        "solar",
                                        "wind_speed",
                                        "wind_direction",
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