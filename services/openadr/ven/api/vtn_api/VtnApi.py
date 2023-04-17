import aiohttp
import logging


class HTTPError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"{status_code}: {message}")


class VtnApi:
    def __init__(self, vtn_base_url: str, timeout: int = 2, headers: dict = {'Content-Type': 'application/json'}
                 ):
        if not vtn_base_url:
            raise ValueError("vtn_measurement_url cannot be None")
        self.vtn_base_url = vtn_base_url
        self.headers = headers
        self.timeout = timeout

    async def put_data(self, path: str, data: dict):
        try:
            url = self.vtn_base_url + path
            async with aiohttp.ClientSession() as session:
                logging.info(f"*********** Send to VTN API: {url} ***********")
                async with session.put(url, json=data, headers=self.headers, timeout=self.timeout) as response:
                    content_type = response.headers.get('Content-Type', '')
                    if response.status == 400:
                        raise HTTPError(400, "Bad Request")
                    elif response.status == 401:
                        raise HTTPError(401, "Unauthorized")
                    elif response.status == 403:
                        raise HTTPError(403, "Forbidden")
                    elif response.status == 404:
                        raise HTTPError(404, "Not Found")
                    elif response.status == 500:
                        raise HTTPError(500, "Internal Server Error")
                    elif response.status == 200:
                        if 'application/json' in content_type:
                            return await response.json()
                        else:
                            return await response.text()
                    else:
                        raise HTTPError(response.status, "Unknown Error")

        except Exception as e:
            raise Exception(f"Error VTN API: {e}")
