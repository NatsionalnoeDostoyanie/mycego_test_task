"""
This module contains views for handling public URL input, displaying file lists, and downloading files from Yandex Disk.
It leverages Django's class-based views to manage interactions with users and the Yandex Disk API.

Key Components:
---------------
1. InputLinkView: Handles the submission of a public URL and redirects to the file list.
2. FileListView: Displays a list of files based on the submitted public URL.
3. DownloadFilesView: Manages the downloading of selected files from Yandex Disk.
"""

import logging
from typing import Any
from urllib.parse import urljoin

from django.http import (
    HttpRequest,
    HttpResponseRedirect,
)
from django.shortcuts import redirect
from django.urls import (
    reverse,
    reverse_lazy,
)
from django.views import View
from django.views.generic import (
    FormView,
    TemplateView,
)

from yandex_disk_project.disk_api.utils import (
    ResourceOperations,
    ResourceRequestParams,
)
from yandex_disk_project.disk_api.v1.forms import PublicUrlInputForm


logger = logging.getLogger(__name__)


class InputLinkView(FormView[PublicUrlInputForm]):
    """
    A view that handles the submission of a public URL.

    This view processes the form submission and redirects the user to the file list page
    with the submitted public URL included in the query parameters.
    """

    template_name = "v1/public_url_input.html"
    form_class = PublicUrlInputForm
    success_url = reverse_lazy("files_list")

    def form_valid(self, form: PublicUrlInputForm) -> HttpResponseRedirect:
        """
        Handles the form submission when valid. Constructs a redirect URL including the public URL.

        :param form: An instance of PublicUrlInputForm containing the validated form data.

        :type form: PublicUrlInputForm

        :return: An HTTP redirect response to the constructed URL.
        :rtype: HttpResponseRedirect

        :raises Exception: If there is an error while constructing the redirect URL.
        """

        public_url = form.cleaned_data["public_url"]
        logger.info(f"Public url received: {public_url}")

        try:
            redirect_to = urljoin(
                self.get_success_url(),
                f"?public_url={public_url}",
            )
            logger.info(f"Redirect to: {redirect_to}")
        except Exception as e:
            logger.error(f"Error while redirecting: {e}")
            raise

        return redirect(redirect_to)


class FileListView(TemplateView):
    """
    A view that displays a list of files based on the public URL.

    This view retrieves the resource data from the Yandex Disk API based on the provided public URL
    and renders the file list template.
    """

    template_name = "v1/file_list.html"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """
        Retrieves context data for rendering the file list page. Fetches resource data using the public URL from
        the request.

        :param kwargs: Additional keyword arguments passed to the method.

        :type kwargs: dict[str, Any]

        :return: A dictionary containing context data, including the resource data.
        :rtype: dict[str, Any]

        :raises Exception: If there is an error while retrieving the resource data.
        """

        context = super().get_context_data(**kwargs)

        public_url: str = self.request.GET.get("public_url", "")
        logger.info(f"Got the public URL from request: {public_url}")

        params = ResourceRequestParams(public_key=public_url)

        try:
            data_dict = ResourceOperations().get_public_resource_dict(params=params)
            logger.info(f"Resource data received")
        except Exception as e:
            logger.error(f"Error while retrieving resource data: {e}")
            raise

        context["data"] = data_dict

        return context


class DownloadFilesView(View):
    """
    A view that handles the downloading of selected files.

    This view processes POST requests to download files based on the provided public key and the list of selected files.
    """

    @staticmethod
    def post(request: HttpRequest) -> HttpResponseRedirect:
        """
        Processes a POST request to download files based on the public key and selected files.

        :param request: The HTTP request object containing the public key and selected files.

        :type request: HttpRequest

        :return: An HTTP redirect response to the file list page with the public URL included.
        :rtype: HttpResponseRedirect

        :raises Exception: If there is an error while downloading the files.
        """

        public_key = request.GET.get("public_key", "")
        selected_files = request.POST.getlist("selected_files")

        logger.info(f"Uploading files. Public key: {public_key}, Selected files: {selected_files}")
        try:
            ResourceOperations().download_files(
                public_key,
                selected_files,
            )
            logger.info(f"Files uploaded successfully")
        except Exception as e:
            logger.error(f"Error while downloading files: {e}")
            raise

        redirect_to = urljoin(
            reverse("files_list"),
            f"?public_url={request.GET.get("public_url", "")}",
        )
        logger.info(f"Redirect to: {redirect_to}")
        return redirect(redirect_to)
