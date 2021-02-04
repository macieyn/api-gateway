import os
import requests
from requests.exceptions import ConnectionError
import json
from flask import Blueprint, request
from flask import current_app as app

from app.auth import login_required

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


services = {
    'books': Service('books', 'books', '5000', 'info'),
    'cars': Service('cars', 'cars', '5000', 'info'),
    'articles': Service('articles', 'articles', '80', 'info'),
    'fake': Service('fake', 'fake', '5000', 'fake'),
}


bp = Blueprint('services', __name__, url_prefix='/services')


@bp.route('/')
def services_info():
    data = { 'services': [] }
    for service in services.values():
        try:
            response = service.info()
            data['services'].append(response)
        except ConnectionError:
            pass
    return data, 200


@bp.route('/<string:service>/<path:path>', methods=('GET', 'POST'))
@login_required
def call_service(service, path):
    if request.method == 'GET':
        data = services[service].get(path)
        return data, 200
    elif request.method == 'POST':
        data, code = services[service].post(path, json=json.dumps(request.json))
        return data, code