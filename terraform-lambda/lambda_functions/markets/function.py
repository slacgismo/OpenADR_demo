import json


def handler(event, context):
    """
    Get /all-markets-status, Get the status of all markets
    get_all_markets_status_handler
    """

    """
    Get /db/markets, Get a list of markets.
    list_markets_handler
    """
    """
    GET /db/market/<market_id>, Get a market by market_id
    get_market_handler
    """
    """
    put_market_handler
    """
    """
    delete_market_handler
    """
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'Hello from market lambda!'})
    }
