"""
This package contains the configuration settings for the Yandex Disk project,
integrating various aspects necessary for the proper functioning of the Djangon project.

Consolidates various configuration files related to the Django project, including application settings,
database configurations, internationalization options, logging settings, middleware, static files, and templates.

Includes a specific call to monkey-patch the Django type stubs for enhanced type checking.

Key Components:
---------------
1. Apps Configuration (apps.py):
   - Contains configuration for Django applications used in the project.
   - Registers apps with specific settings for integration within the Django
     framework.

2. Common Settings (common.py):
   - Defines general settings applicable across different environments.
   - Includes configurations such as DEBUG mode, allowed hosts, and other
     project-wide settings.

3. Database Configuration (db.py):
   - Specifies the database settings required for the application.
   - Includes database engine, name, user credentials, and connection options.

4. Internationalization Settings (i18n.py):
   - Configures language and locale settings for the project.
   - Supports translations and adaptations for international users.

5. Logging Configuration (logging.py):
   - Sets up logging parameters for the application.
   - Configures loggers, handlers, and formatters to capture application logs.

6. Middleware Settings (middleware.py):
   - Defines middleware classes that process requests and responses.
   - Configures middlewares that modify request and response objects or perform
     additional processing.

7. Static Files Settings (static.py):
   - Configures static file handling for the Django project.
   - Defines settings for serving static files such as CSS, JavaScript, and
     images.

8. Template Settings (templates.py):
   - Specifies settings for template engines used in rendering HTML.
   - Configures template directories, loaders, and context processors.
"""

import django_stubs_ext

from yandex_disk_project.settings.apps import *
from yandex_disk_project.settings.common import *
from yandex_disk_project.settings.db import *
from yandex_disk_project.settings.i18n import *
from yandex_disk_project.settings.logging import *
from yandex_disk_project.settings.middleware import *
from yandex_disk_project.settings.static import *
from yandex_disk_project.settings.templates import *


django_stubs_ext.monkeypatch()
