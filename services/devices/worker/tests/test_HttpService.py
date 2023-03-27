import requests
from classes.HttpService import HealthCheckService


def test_health_check():
    # Start the HealthCheckService
    service = HealthCheckService("localhost", 8080, "/health")
    service.run(None, None)

    # Send a request to the health check endpoint
    response = requests.get("http://localhost:8080/health")

    # Check if the response is 200 OK and the body is "OK"
    assert response.status_code == 200
    assert response.text == "OK"
