import json


def handler(event, context):
    """
    PUT /db/resource/<resource_id>?<args>
    put_resource_handler
    """

    """
    GET /db/resource/<resource_id> -- Gets data about a system resource.
    get_resource_handler
    """

    """
    GET /db/resources?<args...>, Get a list of resource ids
    list_resources_handler
    """

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'Hello from weather lambda!'})
    }
