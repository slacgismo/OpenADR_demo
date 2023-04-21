
import uuid


def say_hello():
    return 'Hello world!'


def guid():
    """Return a globally unique id"""
    return uuid.uuid4().hex[2:]
