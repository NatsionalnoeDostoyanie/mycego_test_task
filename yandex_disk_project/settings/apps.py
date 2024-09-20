"""
Settings for registering Django applications and their configurations.
"""

INSTALLED_APPS = [
    "yandex_disk_project.disk_api.v1.apps.DiskApiConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
]
