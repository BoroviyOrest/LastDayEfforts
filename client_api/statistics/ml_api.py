import requests

from utils.ml_api_request import MlApiRequest


class MlApiStatsRequest(MlApiRequest):
    def __init__(self):
        super().__init__(resource='api_calls')

    def filter(self, user_uuid=None, style_id=None, from_datetime=None, to_datetime=None):
        query_params = {}

        if user_uuid is not None:
            query_params['user_uuid'] = user_uuid
        if style_id is not None:
            query_params['style_id'] = style_id
        if from_datetime is not None:
            query_params['from_datetime'] = from_datetime
        if to_datetime is not None:
            query_params['to_datetime'] = to_datetime

        r = requests.get(
            self.url,
            headers=self.headers,
            params=query_params
        )
        return r.json()
