"""
URL configuration for the disk API application.

This module defines the URL patterns for the disk API, including the versioning of the API.

Example URL patterns:
- /v1/ - Base path for version 1 of the disk API.
"""

from django.urls import (
    include,
    path,
)


urlpatterns = [
    path("v1/", include("yandex_disk_project.disk_api.v1.urls"), name="disk_api_v1"),
]
