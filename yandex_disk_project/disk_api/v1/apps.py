"""
This module defines the configuration for the Yandex Disk API interaction app (v1) within the Django project.
It contains the application configuration class used for setting up the app's name and verbose name.
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DiskApiConfig(AppConfig):
    """
    Configuration class for the Yandex Disk API interaction app.

    This class is responsible for setting up the application's name and verbose name,
    which is used in the Django admin and other places where the app is referenced.
    """

    name = "yandex_disk_project.disk_api.v1"
    verbose_name = _("YandexDiskAPI interaction app")
