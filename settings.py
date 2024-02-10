from pathlib import Path
from dotenv import dotenv_values

ROOT_DIR = Path('__file__').parent

environ = {}

if (ROOT_DIR / '.env').exists():
    environ = {**dotenv_values(str(ROOT_DIR / '.env'))}

POSTGRES_URL = environ.get('POSTGRES_URL', 'postgres://dev:dev@192.168.0.16:5432/forms')
REDIS_URL = environ.get('REDIS_URL', 'redis://localhost:6379/0')
DEBUG = environ.get('DEBUG', False)

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

DEBUG = DEBUG
