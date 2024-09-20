"""
This module defines the URL routing for the Yandex Disk API interaction app (v1).
It maps URL paths to specific view classes that handle requests related to Yandex Disk operations.
"""

from django.urls import path

from yandex_disk_project.disk_api.v1.views import (
    DownloadFilesView,
    FileListView,
    InputLinkView,
)


urlpatterns = [
    path("", InputLinkView.as_view(), name="disk_api_view"),
    path("files/", FileListView.as_view(), name="files_list"),
    path("download/", DownloadFilesView.as_view(), name="download_files"),
]
