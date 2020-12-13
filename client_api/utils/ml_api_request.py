from abc import ABC

import requests
from django.conf import settings

from utils.redis import RedisClient


class MlApiRequest(ABC):
    def __init__(self, resource=''):
        self._api_host = settings.ML_API_HOST
        self._api_port = settings.ML_API_PORT
        self._api_key = settings.ML_API_KEY
        self._jwt = RedisClient().token
        self._resource = resource

    @property
    def base_url(self):
        return f'http://{self._api_host}:{self._api_port}'

    @property
    def url(self):
        return f'{self.base_url}/{self._resource}'

    @property
    def headers(self):
        return {'Authorization': f'Bearer {self._jwt}'}

    def retrieve(self, instance_id):
        r = requests.get(f'{self.url}/{instance_id}', headers=self.headers)
        return r.json()

    def list(self):
        r = requests.get(self.url, headers=self.headers)
        return r.json()

    def post(self, **kwargs):
        pass

    def put(self, **kwargs):
        pass

    def patch(self, instance_id, **kwargs):
        pass

    def refresh_token(self):
        data = {
            'email': settings.ML_API_USER,
            'password': settings.ML_API_PASSWORD
        }
        r = requests.post(f'{self.base_url}/users/login', json=data)
        return r.json().get('token', '')
