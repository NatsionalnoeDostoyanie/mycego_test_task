"""
Common and general settings.
"""

import os

import environ
from dotenv import load_dotenv


load_dotenv()
env = environ.Env()

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "..",
        "..",
    ),
)

ROOT_URLCONF = "core.urls"

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = env.bool(
    "DEBUG",
    default=True,
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
