import requests
from requests.exceptions import ConnectionError
import json

class Service:
    
    def __init__(self, name, host, port, info_endpoint):
        self.name = name
        self.host = host
        self.port = port 
        self.info_endpoint = info_endpoint
        self.request = requests

    def info(self):
        try:
            response = self.request.get(f"http://{self.host}:{self.port}/{self.info_endpoint}")
            return json.loads(response.text)
        except ConnectionError:
            raise 

    def ping(self):
        try:
            self.request.get(f"http://{self.host}:{self.port}/{self.info_endpoint}")
            return True
        except ConnectionError:
            return False

    def get(self, endpoint):
        try:
            response = self.request.get(f"http://{self.host}:{self.port}/{endpoint}")
            return json.loads(response.text)
        except ConnectionError:
            raise
            

    def post(self, endpoint, **kwargs):
        try:
            response = self.request.post(f"http://{self.host}:{self.port}/{endpoint}", **kwargs)
            return json.loads(response.text)
        except ConnectionError:
            raise
