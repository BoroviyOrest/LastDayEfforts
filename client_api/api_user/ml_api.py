import requests

from utils.ml_api_request import MlApiRequest


class MlApiUserRequest(MlApiRequest):
    def __init__(self):
        super().__init__(resource='admin')

    def patch(self, instance_id, calls_per_day_limit=None, is_active=None, is_admin=None):
        body = {
            'calls_per_day_limit': calls_per_day_limit,
            'is_active': is_active,
            'is_admin': is_admin}
        r = requests.patch(
            f'{self.url}/{instance_id}',
            headers=self.headers,
            json=body
        )
        return r.json()
