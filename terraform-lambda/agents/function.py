import json


def handler(event, context):
    """
    list of agents
    Get /db/agents?resource_id=<resource_id>&valid_at=<valid_at>, Get a list of agents id
    """
    """
    get one agent
    Get /db/agent/{agent_id}, Get an agent info. If there is already a record for <agent_id>,
    then it returns the previous data entry. Otherwise, return the new data entry.
    """
    """
    PUT /db/agent/{agent_id}?resource_id=<resource_id>
    Put an agent record to table
    """
    """
    PUT /agent/{agent_id}?resource_id=<resource_id>
    Put an agent record to simulation table
    """
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'Hello from Lambda!'})
    }
