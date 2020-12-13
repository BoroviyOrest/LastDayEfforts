import requests

from utils.ml_api_request import MlApiRequest


class MlApiStyleRequest(MlApiRequest):
    def __init__(self):
        super().__init__(resource='style')

    def post(self, description):
        r = requests.post(
            self.url,
            headers=self.headers,
            json={'description': description}
        )
        return r.json()

    def put(self, instance_id, description):
        r = requests.put(
            f'{self.url}/{instance_id}',
            headers=self.headers,
            json={'description': description}
        )
        print(r.json())
        return r.json()
