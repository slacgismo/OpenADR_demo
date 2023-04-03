
import requests


class ErrorHandling:

    def __init__(self):
        pass

    def handle(self, error):
        if isinstance(error, requests.exceptions.RequestException):
            # HTTP errors
            if isinstance(error, requests.exceptions.HTTPError):
                print("HTTP Error:", error)
            elif isinstance(error, requests.exceptions.ConnectionError):
                print("Connection Error:", error)
            elif isinstance(error, requests.exceptions.Timeout):
                print("Timeout Error:", error)
            elif isinstance(error, requests.exceptions.TooManyRedirects):
                print("Too Many Redirects Error:", error)
            # Other Request errors
            else:
                print("Request Error:", error)
        # Common Python errors
        elif isinstance(error, ValueError):
            print("Value Error:", error)
        elif isinstance(error, TypeError):
            print("Type Error:", error)
        elif isinstance(error, NameError):
            print("Name Error:", error)
        elif isinstance(error, ZeroDivisionError):
            print("Zero Division Error:", error)
        elif isinstance(error, IndexError):
            print("Index Error:", error)
        else:
            print("Unknown Error:", error)
