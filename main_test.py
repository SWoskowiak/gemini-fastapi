"""Test the main FastAPI app."""
# pylint: disable=line-too-long

import unittest.mock
from types import SimpleNamespace
from fastapi.testclient import TestClient
from sqlalchemy import select, MetaData, Table
import pytest
from main import app
from db import db

@pytest.fixture(name="client")
def client_fixture():
    """Create a test client for using in our tests that will use our FastAPI main app definition."""
    return TestClient(app)

# NOTE: This fixture will be used by all tests in this file. It will truncate the database before each test.
@pytest.fixture(autouse=True)
def truncate_database():
    """Clear the database before each test."""
    db.truncate_all()
    yield

# NOTE: Note the autouse=True here. All tests in this file will use this fixture.
# While auto-use fixtures are generally discouraged we definitely don't want tests to ever call the google API directly.
@pytest.fixture(name="_stubbed_generate_content_async", autouse=True)
def stubbed_generate_content_async_fixture():
    """Don't actually call the gemini API when testing so return a mock response instead."""
    with unittest.mock.patch("gemini.model.generate_content_async", return_value=SimpleNamespace(text="mock response")) as mock:
        yield mock

# NOTE: Note the autouse=True here. All tests in this file will use this fixture.
# We don't want to actually upload files to the cloud storage bucket when testing so return a mock response instead.
@pytest.fixture(name="_stubbed_upload_file", autouse=True)
def stubbed_upload_file_fixture():
    """Don't actually call upload_file when testing so return a mock response instead."""
    with unittest.mock.patch("google_cloud.upload_file", return_value="12345_mockImage.jpg") as mock:
        yield mock

# NOTE: Note the autouse=True here. All tests in this file will use this fixture.
# We don't want to actually upload files to the cloud storage bucket when testing so return a mock response instead.
@pytest.fixture(name="_stubbed_upload_file_bytestream", autouse=True)
def stubbed_upload_file_bytestream_fixture():
    """Don't actually call upload_file when testing so return a mock response instead."""
    with unittest.mock.patch("google_cloud.upload_file_bytestream", return_value="12345_mockImage.jpg") as mock:
        yield mock

# We don't need to make thumbnails when testing upload since we are not sending them to google storage
@pytest.fixture(name="_stubbed_make_thumbnail")
def stubbed_make_thumbnail_fixture():
    """Don't actually call upload_file when testing so return a mock response instead."""
    with unittest.mock.patch("image_util.make_thumbnail", return_value=b"mockThumbnailBytes") as mock:
        yield mock

def test_upload_image(client, _stubbed_make_thumbnail):
    """Happy path test for uploading an image"""
    response = client.post(
        "/upload/",
        files={"image": ("test.jpg", b"pretend image bytes", "image/jpeg")},
        data={"prompt": "test prompt"}
    )

    gemini_queries = Table('gemini_queries', MetaData(), autoload_with=db.engine)
    with db.get_session() as session:
        result = session.execute(select(gemini_queries)).fetchone()

    assert result.original_filename == "test.jpg"
    assert result.prompt == "test prompt"

    assert response.status_code == 200
    assert response.text == "mock response"

def test_upload_image_no_prompt(client, _stubbed_make_thumbnail):
    """Test for uploading an image without a prompt"""
    response = client.post(
        "/upload/",
        files={"image": ("test.jpg", b"pretend image bytes", "image/jpeg")},
        # NOTE: No prompt
    )
    assert response.status_code == 422
