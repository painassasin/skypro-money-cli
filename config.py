from pathlib import Path

from environs import env

BASE_DIR = Path.cwd()

env.read_env()

SKYPRO_EMAIL = env('SKYPRO_EMAIL')
SKYPRO_PASSWORD = env('SKYPRO_PASSWORD')
SKYPRO_BASE_URL = 'https://operation-planning.sky.pro'
SKYPRO_LOGIN_URL = '/careusers/login/'
SKYPRO_CSRF_COOKIE_NAME = 'csrftoken'
SKYPRO_TIMEOUT_IN_SECONDS = 2
