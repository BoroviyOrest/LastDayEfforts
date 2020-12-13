import pickle

from django.conf import settings
from redis import Redis


class RedisClient:
    def __init__(self):
        self._client = Redis(**settings.REDIS)

    @property
    def token(self):
        return self._client.get('access_token')

    def update_token(self, value):
        self._client.set('access_token', value)

    def publish_to_socketio(self, image_url, image_id):
        message = {
            'method': 'emit',
            'event': 'message',
            'namespace': '/',
            'room': image_id,
            'data': {
                'image_url': image_url
            }

        }
        pickled_message = pickle.dumps(message)
        self._client.publish('socketio', pickled_message)

        close_data = {
            'method': 'close_room',
            'namespace': '/',
            'room': image_id,
        }
        pickled_close_data = pickle.dumps(close_data)
        self._client.publish('socketio', pickled_close_data)
