import os
from dotenv import dotenv_values

ROOT_DIR = src_path = os.path.dirname(os.path.abspath(__file__))

environ = {}

if os.path.exists(os.path.join(ROOT_DIR, '.env')):
    environ = {**dotenv_values(os.path.join(ROOT_DIR, '.env'))}

environ.update(**os.environ)
POSTGRES_HOST = environ.get('POSTGRES_HOST', '127.0.0.1')

POSTGRES_URL = environ.get('POSTGRES_URL', f'postgres://dev:dev@{POSTGRES_HOST}:5432/courses')

REDIS_HOST = environ.get('REDIS_HOST', '127.0.0.1')
QUEUE_NAME = 'courses'
RABBITMQ_HOST = environ.get('RABBITMQ_HOST', '127.0.0.1')

RABBITMQ_URL = environ.get('RABBITMQ_URL', f'amqp://guest:guest@{RABBITMQ_HOST}/')

DEBUG = environ.get('DEBUG', False)

KEY_COURSES_REDIS = environ.get('KEY_COURSES_REDIS', 'courses:symbol')

COINGECKO_API_KEY = environ.get('COINGECKO_API_KEY', 'CG-S3XwimKvYK4gNNinMXP4HVS4')

TORTOISE_ORM = {
    'connections': {
        'default': POSTGRES_URL
    },
    'apps': {
        'models': {
            'models': ['models', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}