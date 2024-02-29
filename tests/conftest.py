from datetime import datetime
from typing import Any, Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from file_server import app as file_server_app

from settings import MEDIA_DIR


@pytest.fixture
def media_dir() -> Generator[None, Any, Any]:
    start_time = datetime.now().timestamp()
    yield
    for item in MEDIA_DIR.glob('*'):
        if item.stat().st_ctime >= start_time:
            item.unlink(missing_ok=True)


@pytest.fixture
def app(media_dir) -> Generator[Flask, Any, Any]:
    yield file_server_app


@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()
