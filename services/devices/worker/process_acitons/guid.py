import uuid


def guid():
    """Return a globally unique id"""
    return uuid.uuid4().hex[2:]
