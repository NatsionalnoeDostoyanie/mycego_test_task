"""
This module provides functionality for interacting with the Yandex Disk API, specifically for handling public resources.
It includes classes for constructing requests to the API, managing response parameters,
and downloading files from public urls.

Key Components:
---------------
1. ResourceRequestParams:
   A dataclass that encapsulates parameters for requesting resources from the Yandex Disk API.
   It allows specifying sorting options, preview sizes, fields to include in responses,
   and other relevant query parameters.

2. ResourceOperations:
   A class that provides methods to interact with Yandex Disk public resources,
   including fetching resource data and downloading files.
   It constructs the necessary API URLs and handles responses, including error management and logging.
"""

import logging
import os
from dataclasses import (
    asdict,
    dataclass,
)
from enum import (
    StrEnum,
    unique,
)
from pathlib import Path
from typing import (
    Any,
    Optional,
    Union,
)
from urllib.parse import (
    quote,
    urlencode,
    urljoin,
)

import requests
from dotenv import load_dotenv

from yandex_disk_project.settings import BASE_DIR


load_dotenv()

logger = logging.getLogger(__name__)


@dataclass
class ResourceRequestParams:
    """
    Parameters for requesting resources from Yandex Disk API.

    This class encapsulates the parameters required to make requests to the Yandex Disk API, allowing
    for flexible configuration of sorting, preview sizes, and fields to include in the API response.
    """

    @unique
    class SortOptions(StrEnum):
        """
        Options for sorting resources.

        Supports specifying the sort order.

        Available sorting options include:
        - CREATED: Sort by creation date.
        - MODIFIED: Sort by modification date.
        - NAME: Sort by resource name.
        - PATH: Sort by resource path.
        - SIZE: Sort by resource size.

        To specify the descending sort use:
        `SortOptions.<sort option>.desc`.
        """

        CREATED = "created"
        MODIFIED = "modified"
        NAME = "name"
        PATH = "path"
        SIZE = "size"

        @property
        def desc(self) -> str:
            """
            Returns the descending order representation of the sorting option.

            :return: Sorting option prefixed with a minus sign.
            :rtype: str
            """

            return f"-{self}"

    @unique
    class PreviewSizeOptions(StrEnum):
        """
        Options for preview sizes.

        The image will be scaled to fit the specified dimension, preserving the original aspect ratio.

        Supports specifying custom resolution using the `resolution()` method.

        Available sizes:
        - S: 150 pixels
        - M: 300 pixels
        - L: 500 pixels
        - XL: 800 pixels
        - XXL: 1024 pixels
        - XXXL: 1280 pixels
        """

        # fmt: off
        S = "S"        # 150 pixels
        M = "M"        # 300 pixels
        L = "L"        # 500 pixels
        XL = "XL"      # 800 pixels
        XXL = "XXL"    # 1024 pixels
        XXXL = "XXXL"  # 1280 pixels
        # fmt: on

        @staticmethod
        def resolution(width: Optional[int] = None, height: Optional[int] = None) -> str:
            """
            Returns the resolution in the format "<width>x<height>".

            Only one dimension can be specified, or both. Raises ValueError for invalid formats.

            :param width: The width of the preview in pixels.
            :param height: The height of the preview in pixels.

            :type width: Optional[int]
            :type height: Optional[int]

            :return: Resolution in "<width>x<height>" format.
            :rtype: str

            :raises ValueError: If the input format is invalid.
            """

            # fmt: off
            # Only for Python >3.10
            match (width, height):
                case (int(w), int(h)):  # '<integer>, <integer>'
                    return f"{w}x{h}"
                case (int(w), None):    # '<integer>, None'
                    return f"{w}x"
                case (None, int(h)):    # 'None, <integer>'
                    return f"x{h}"
                case _:
                    raise ValueError(
                        "Invalid input format, expected '<integer>, <integer>', '<integer>, None', or 'None, <integer>'"
                    )
            # fmt: on

    @unique
    class FieldOptions(StrEnum):
        """
        Options for specifying fields to include in the response from the Yandex Disk API.

        Each option corresponds to a specific attribute of the resource.
        """

        # Resource options
        ANTIVIRUS_STATUS = ".antivirus_status"
        COMMENT_IDS = ".comment_ids"
        CREATED = ".created"
        CUSTOM_PROPERTIES = ".custom_properties"
        EMBEDDED = "._embedded"
        EXIF = ".exif"
        FILE = ".file"
        MD5 = ".md5"
        MEDIA_TYPE = ".media_type"
        MIME_TYPE = ".mime_type"
        MODIFIED = ".modified"
        NAME = ".name"
        ORIGIN_PATH = ".origin_path"
        OWNER = ".owner"
        PATH = ".path"
        PREVIEW = ".preview"
        PUBLIC_KEY = ".public_key"
        PUBLIC_URL = ".public_url"
        RESOURCE_ID = ".resource_id"
        REVISION = ".revision"
        SHA256 = ".sha256"
        SIZE = ".size"
        SIZES = ".sizes"
        TYPE = ".type"
        VIEWS_COUNT = ".views_count"

        # Embedded items options
        EMBEDDED_ITEMS = EMBEDDED + ".items"
        EMBEDDED_LIMIT = EMBEDDED + ".limit"
        EMBEDDED_OFFSET = EMBEDDED + ".offset"
        EMBEDDED_PATH = EMBEDDED + PATH
        EMBEDDED_PUBLIC_KEY = EMBEDDED + PUBLIC_KEY
        EMBEDDED_SORT = EMBEDDED + ".sort"
        EMBEDDED_TOTAL = EMBEDDED + ".total"

        # Specific embedded items options
        EMBEDDED_ITEMS_ANTIVIRUS_STATUS = EMBEDDED_ITEMS + ANTIVIRUS_STATUS
        EMBEDDED_ITEMS_COMMENT_IDS = EMBEDDED_ITEMS + COMMENT_IDS
        EMBEDDED_ITEMS_CREATED = EMBEDDED_ITEMS + CREATED
        EMBEDDED_ITEMS_CUSTOM_PROPERTIES = EMBEDDED_ITEMS + CUSTOM_PROPERTIES
        EMBEDDED_ITEMS_EXIF = EMBEDDED_ITEMS + EXIF
        EMBEDDED_ITEMS_FILE = EMBEDDED_ITEMS + FILE
        EMBEDDED_ITEMS_MD5 = EMBEDDED_ITEMS + MD5
        EMBEDDED_ITEMS_MEDIA_TYPE = EMBEDDED_ITEMS + MEDIA_TYPE
        EMBEDDED_ITEMS_MIME_TYPE = EMBEDDED_ITEMS + MIME_TYPE
        EMBEDDED_ITEMS_MODIFIED = EMBEDDED_ITEMS + MODIFIED
        EMBEDDED_ITEMS_NAME = EMBEDDED_ITEMS + NAME
        EMBEDDED_ITEMS_PATH = EMBEDDED_ITEMS + PATH
        EMBEDDED_ITEMS_PREVIEW = EMBEDDED_ITEMS + PREVIEW
        EMBEDDED_ITEMS_PUBLIC_KEY = EMBEDDED_ITEMS + PUBLIC_KEY
        EMBEDDED_ITEMS_PUBLIC_URL = EMBEDDED_ITEMS + PUBLIC_URL
        EMBEDDED_ITEMS_RESOURCE_ID = EMBEDDED_ITEMS + RESOURCE_ID
        EMBEDDED_ITEMS_REVISION = EMBEDDED_ITEMS + REVISION
        EMBEDDED_ITEMS_SHA256 = EMBEDDED_ITEMS + SHA256
        EMBEDDED_ITEMS_SIZE = EMBEDDED_ITEMS + SIZE
        EMBEDDED_ITEMS_SIZES = EMBEDDED_ITEMS + SIZES
        EMBEDDED_ITEMS_TYPE = EMBEDDED_ITEMS + TYPE

    FieldsType = Union[
        FieldOptions,
        tuple[FieldOptions, ...],
    ]
    FilteredDictType = dict[
        str,
        Union[
            str,
            int,
            bool,
            FieldsType,
            SortOptions,
            PreviewSizeOptions,
        ],
    ]

    # fmt: off
    public_key: str                                    # A public key for the Yandex Disk resource (required parameter)
    fields: Optional[FieldsType] = None                # Attributes to include in the response. Can be a single/tuple
    limit: Optional[int] = 1_000_000_000_000_000_000   # Limit on the number of resources returned
    offset: Optional[int] = None                       # Offset from the beginning of the list of resources
    path: Optional[str] = None                         # Relative path starting with "/"
    preview_crop: Optional[bool] = None                # Indicates whether to crop the preview
    preview_size: Optional[PreviewSizeOptions] = None  # Size of the preview
    sort: Optional[SortOptions] = None                 # Sorting option. Use `.desc` for descending order
    # fmt: on

    @property
    def prepared_dict(self) -> FilteredDictType:
        """
        Returns a dictionary of the parameters without `None` values and and formatting fields as a CSV string..

        :return: Dictionary of parameters with formatted fields.
        :rtype: FilteredDictType
        """

        result = {k: v for k, v in asdict(self).items() if v is not None}
        if isinstance(self.fields, tuple):
            result["fields"] = ",".join(field.value[1:] for field in self.fields)

        return result


class ResourceOperations:
    """
    Operations for interacting with Yandex Disk public resources.

    Provides methods to fetch resource data and download files from a public Yandex Disk url.
    It constructs the necessary URLs and handles the API interactions required to perform these operations.
    """

    YANDEX_DISK_PUBLIC_RESOURCES_BASE_URL = os.getenv(
        "YANDEX_DISK_PUBLIC_RESOURCES_BASE_URL",
        "https://cloud-api.yandex.net/v1/disk/public/resources/",
    )
    PROJECT_DIR = os.path.join(
        BASE_DIR,
        "..",
    )

    FILES_DIR = os.path.join(
        PROJECT_DIR,
        "files",
    )

    def get_public_resource_dict(self, params: ResourceRequestParams) -> dict[str, Any]:
        """
        Fetches resource data from Yandex Disk API based on the provided parameters.

        :param params: Parameters for the resource request.

        :type params: ResourceRequestParams

        :return: Dictionary containing the resource data.
        :rtype: dict[str, Any]

        :raises Exception: If there is an error fetching the resource data.
        """

        if params.fields is None:
            # Setting default fields required for current specific functionality.

            # These fields are not mandatory but improve the efficiency of data generation on Yandex's side.

            # Specifying these fields ensures that the response contains the minimum necessary information
            # for current application to function correctly.
            params.fields = (
                ResourceRequestParams.FieldOptions.NAME,
                ResourceRequestParams.FieldOptions.PUBLIC_URL,
                ResourceRequestParams.FieldOptions.EMBEDDED_ITEMS_NAME,
                ResourceRequestParams.FieldOptions.EMBEDDED_ITEMS_TYPE,
                ResourceRequestParams.FieldOptions.EMBEDDED_ITEMS_MEDIA_TYPE,
                ResourceRequestParams.FieldOptions.EMBEDDED_ITEMS_PUBLIC_URL,
                ResourceRequestParams.FieldOptions.PATH,
            )

        query_params = urlencode(params.prepared_dict)
        full_url = urljoin(self.YANDEX_DISK_PUBLIC_RESOURCES_BASE_URL, f"?{query_params}")
        logger.info(f"Full URL for fetching public resource: {full_url}")

        data_json: dict[str, Any] = requests.get(full_url).json()
        logger.info("Successfully fetched public resource data.")

        # Renaming the '_embedded' key to 'embedded' to ensure compatibility with templates.

        # Some templates may not recognize context parameters with underscore at the beginning of a word as a valid key,
        # so this renaming ensures that the response data is in the expected format.
        if "_embedded" in data_json:
            data_json["embedded"] = data_json.pop("_embedded")
            logger.info("Renamed '_embedded' to 'embedded' in response data.")

        return data_json

    def download_files(self, public_key: str, files_paths: list[str]) -> None:
        """
        Downloads files from a public Yandex Disk url.

        :param public_key: Public key for the disk or directory.
        :param files_paths: List of relative paths to the files to be downloaded.

        :type public_key: str
        :type files_paths: list[str]

        :return: None
        :rtype: None

        :raises Exception: If there is an error downloading any of the files.
        """

        new_public_key = quote(public_key.replace(" ", "+"))
        for file_path in files_paths:
            full_url = urljoin(
                urljoin(self.YANDEX_DISK_PUBLIC_RESOURCES_BASE_URL, "download"),
                f"?public_key={new_public_key}&path={quote(file_path)}",
            )
            logger.info(f"Full URL for downloading file: {full_url}")

            response = requests.get(full_url)

            try:
                response_content = requests.get(response.json()["href"])

                # Create a directory if it doesn't exist
                Path(self.FILES_DIR).mkdir(
                    parents=True,
                    exist_ok=True,
                )

                file_local_path = os.path.join(self.FILES_DIR, file_path[1:])
                with open(file_local_path, "wb") as f:
                    f.write(response_content.content)
                logger.info(f"INFO: File downloaded successfully: {file_local_path}")
            except Exception as e:
                logger.error(f"Failed to download file {file_path}: {e}")
