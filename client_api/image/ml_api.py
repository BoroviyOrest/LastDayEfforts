import uuid

import requests
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile

from utils.ml_api_request import MlApiRequest


class MlApiImageRequest(MlApiRequest):
    def __init__(self):
        super().__init__(resource='image')

    @property
    def url(self):
        return f'{self.base_url}/{self._resource}/{self._api_key}'

    def retrieve(self, instance_id):
        r = requests.get(f'{self.url}/{instance_id}', headers=self.headers)
        if r.headers.get('content-type') == 'application/json':
            return
        image = SimpleUploadedFile(
            f'{uuid.uuid4()}.{r.headers["content-type"].split("/")[-1]}',
            r.content,
            r.headers['content-type']
        )
        return image

    def transform_image(self, image_file, style_id):
        files = {'file': (image_file, open(image_file, 'rb'), 'image/png')}
        r = requests.post(self.url, files=files, params={'style_id': style_id})

        if r.status_code == 201:
            return r.json()
