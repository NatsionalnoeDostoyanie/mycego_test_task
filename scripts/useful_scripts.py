"""
This module provides command-line utilities for managing the project.

It supports running the Django development server, performing type checks
with mypy, and running code formatters with isort and black.

Usage:
useful_scripts.py [runserver | mypy | linters]
"""

import logging
import os
import subprocess
import sys

from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.DEBUG)

DJANGO_PROJECT_NAME = os.environ["DJANGO_PROJECT_NAME"]

PROJECT_DIR = os.path.join(
    os.path.abspath(__file__),
    "..",
    "..",
)

TOML_DIR = os.path.join(
    PROJECT_DIR,
    "pyproject.toml",
)


def run_django_server() -> None:
    """
    Runs the Django development server.

    Changes the directory to the Django project directory and executes the `manage.py runserver` command.

    :return: None
    :rtype: None
    """

    logging.info("Running django server")
    _change_directory_and_run(
        ["python", "manage.py", "runserver"],
        os.path.join(PROJECT_DIR, DJANGO_PROJECT_NAME),
    )


def run_linters() -> None:
    """
    Runs code formatters: isort and black.

    Changes the directory to the project directory and executes `isort .` followed by `black .` to format the code.

    :return: None
    :rtype: None
    """

    logging.info("Running isort")
    _change_directory_and_run(["isort", "."])

    logging.info("Running black")
    _change_directory_and_run(["black", "."])


def run_mypy() -> None:
    """
    Runs type checking with mypy.

    Sets the `MYPYPATH` env variable to the project directory and executes `mypy .` with the `.toml` configuration file.

    :return: None
    :rtype: None
    """

    logging.info("Running mypy")
    os.environ["MYPYPATH"] = PROJECT_DIR
    _change_directory_and_run(["mypy", "--config-file", TOML_DIR, "--explicit-package-bases", "."])


def _change_directory_and_run(_console_command: list[str], dir_to_go_to: str = PROJECT_DIR) -> None:
    """
    Changes the current working directory and runs a console command.

    :param _console_command: Command to run as a list of strings.
    :param dir_to_go_to: Directory to change to before running the command. Defaults to PROJECT_DIR.

    :return: None
    :rtype: None
    """

    logging.debug(f"Changing directory to {os.path.abspath(dir_to_go_to)}")
    os.chdir(dir_to_go_to)
    subprocess.run(_console_command)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("Usage: script.py [runserver | mypy | linters]")
        sys.exit(1)

    # Only for Python >3.10
    console_command = sys.argv[1]
    match console_command:
        case "runserver":
            run_django_server()
        case "linters":
            run_linters()
        case "mypy":
            run_mypy()
        case _:
            logging.error(f"Unknown command: {console_command}")
