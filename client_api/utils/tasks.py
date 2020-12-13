from celery.schedules import crontab
from celery.task import Task, PeriodicTask
from django.conf import settings

from image.ml_api import MlApiImageRequest
from image.models import TransformedImage
from utils.ml_api_request import MlApiRequest
from utils.redis import RedisClient


class GetTransformedImage(Task):
    max_retries = None
    default_retry_delay = 10

    def run(self, ml_api_image_id, instance_id):
        image = MlApiImageRequest().retrieve(ml_api_image_id)
        if image is None:
            self.retry()

        try:
            transformed_image = TransformedImage.objects.get(pk=instance_id)
            transformed_image.file = image
            transformed_image.save()

            RedisClient().publish_to_socketio(transformed_image.file.name, transformed_image.id)
        except TransformedImage.DoesNotExist:
            return


class UpdateAccessToken(PeriodicTask):
    run_every = crontab(**settings.ACCESS_TOKEN_UPDATE_PERIOD)

    def run(self, *args, **kwargs):
        redis = RedisClient()
        token = MlApiRequest().refresh_token()
        redis.update_token(token)
