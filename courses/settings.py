import os
from dotenv import dotenv_values

ROOT_DIR = src_path = os.path.dirname(os.path.abspath(__file__))

environ = {}

if os.path.exists(os.path.join(ROOT_DIR, '.env')):
    environ = {**dotenv_values(os.path.join(ROOT_DIR, '.env'))}

REDIS_URL = environ.get('REDIS_URL', 'redis://127.0.0.1:6379')
QUEUE_NAME = 'courses'
RABBIT_MQ = environ.get('RABBIT_MQ', 'amqp://guest:guest@127.0.0.1/')

DEBUG = environ.get('DEBUG', False)

KEY_COURSES_REDIS = environ.get('KEY_COURSES_REDIS', 'courses:symbol')

COINGECKO_API_KEY = environ.get('COINGECKO_API_KEY', 'CG-S3XwimKvYK4gNNinMXP4HVS4')