from enum import Enum
import time


class TESSError:
    def __init__(self, msg, exception=None):
        self.msg = msg
        self.exception = exception

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.msg


class AuctionsAttributes(Enum):
    auction_id = 'auction_id'
    market_id = 'market_id'
    clearing_time = 'clearing_time'
    expected_price = 'expected_price'
    expected_stdev = 'expected_stdev'
    reference_price = 'reference_price'
    price = 'price'
    quantity = 'quantity'
    marginal_type = 'marginal_type'
    marginal_order = 'marginal_order'
    marginal_quantity = 'marginal_quantity'
    marginal_rank = 'marginal_rank'
    valid_at = 'valid_at'


AuctionsAttributesTypes = {
    AuctionsAttributes.auction_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AuctionsAttributes.market_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AuctionsAttributes.clearing_time.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    AuctionsAttributes.expected_price.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    AuctionsAttributes.expected_stdev.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    AuctionsAttributes.reference_price.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    AuctionsAttributes.price.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    AuctionsAttributes.quantity.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    AuctionsAttributes.marginal_type.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AuctionsAttributes.marginal_order.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AuctionsAttributes.marginal_quantity.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AuctionsAttributes.marginal_rank.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AuctionsAttributes.valid_at.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


def create_item(
        primary_key_name: str,
        primary_key_value: str,
        request_body: dict = None,
        attributeType: dict = None,
        attributes: Enum = None,
):
    item = {}

    valid_at = str(int(time.time()))
    for attribute_name, attribute_info in attributeType.items():
        if attribute_name == attributes.valid_at.name:
            item[attribute_name] = {
                attribute_info['dynamodb_type']: valid_at
            }
        elif attribute_name == primary_key_name:
            item[attribute_name] = {
                attribute_info['dynamodb_type']: primary_key_value
            }
        else:
            value = request_body.get(attribute_name, None)
            if value is None:
                raise KeyError(f"{attribute_name} is missing in request body")
            item[attribute_name] = {
                attribute_info['dynamodb_type']: value
            }
    return item


def main():
    request_body = {
        'market_id': '456',
        'clearing_time': 123,
        'expected_price': 123.0,
        'expected_stdev': 123.0,
        'reference_price': 123.0,
        'price': 123.0,
        'quantity': 123.0,
        'marginal_type': '123',
        'marginal_order': '123',
        'marginal_quantity': '123',
        'marginal_rank': '123',
    }
    item = create_item(
        primary_key_name='auction_id',
        primary_key_value='123',
        request_body=request_body,
        attributeType=AuctionsAttributesTypes,
        attributes=AuctionsAttributes
    )
    path1 = "/STAGING/db/agents/query"
    path2 = "/STAGING/db/agents"
    route1 = get_path(path1, 4)
    route2 = get_path(path2, 4)
    print(route1, route2)
    if match_path(path2, "agents"):
        print("match, agents")
    if match_path(path2, "agents/query"):
        print("match, agents/query")


def get_path(path: str, index: int = 0):

    path_parts = path.split('/')
    if index < len(path_parts):
        return path_parts[index]
    else:
        return None


def match_path(path: str, route_key: str) -> bool:
    if "/db/" in path:
        path_suffix = path.split("/db/")[1]
        if path_suffix == route_key:
            return True
    return False


if __name__ == '__main__':
    main()
