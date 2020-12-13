from starlette.config import environ


POSTGRES_DSN = environ.get("POSTGRES_DSN")
POSTGRES_HOST = environ.get("POSTGRES_HOST")
POSTGRES_PORT = environ.get("POSTGRES_PORT")

POSTGRES_USER = environ["POSTGRES_USER"]
POSTGRES_PASSWORD = environ["POSTGRES_PASSWORD"]
POSTGRES_DB = environ["POSTGRES_DB"]

POSTGRES_CONNECTION_MIN_SIZE = environ.get("POSTGRES_CONNECTION_MIN_SIZE", 10)
POSTGRES_CONNECTION_MAX_SIZE = environ.get("POSTGRES_CONNECTION_MAX_SIZE", 10)


SECRET_KEY = environ.get("SECRET_KEY")

ALLOWED_MIME_TYPES = ("image/gif", "image/png", "image/jpeg", "image/bmp")
RAW_IMAGES_DIR = "/data/raw_images"
TRANSFORMED_IMAGES_DIR = "/data/transformed_images"

RABBITMQ_HOST = environ.get("RABBITMQ_HOST")
RABBITMQ_USER = environ.get("RABBITMQ_DEFAULT_USER")
RABBITMQ_PASSWORD = environ.get("RABBITMQ_DEFAULT_PASS")
RABBITMQ_VHOST = environ.get("RABBITMQ_DEFAULT_VHOST")

CELERY_BROKER_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:5672/{RABBITMQ_VHOST}"
CELERY_IGNORE_RESULT = True
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = "Europe/Kiev"
