import boto3


class STSService:
    """
    Get AWS account ID
    """

    def __init__(self):
        self.client = boto3.client('sts')

    def get_account_id(self):
        response = self.client.get_caller_identity()
        account_id = response['Account']
        return account_id
