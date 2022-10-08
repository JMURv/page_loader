import pytest
import os
import tempfile
import requests_mock
from page_loader import url_to_name
from page_loader import download
from pathlib import Path


def get_fixture_path(name):
    return os.path.join('page_loader', 'tests', 'fixtures', name)


def test_correct_name():
    file_path = url_to_name('https://ru.hexlet.io/courses')
    assert file_path == 'ru-hexlet-io-courses.html'


@pytest.mark.parametrize(
    ("url", "fixture_path"),
    [
        (
            "https://ru.hexlet.io/courses",
            'ru-hexlet-io-courses.html'
        ),
    ]
)
def test_download(url, fixture_path):
    fixture_path = get_fixture_path(fixture_path)
    with requests_mock.Mocker() as m:
        with open(fixture_path, 'r', encoding='UTF8') as f:
            m.get(url, text=f.read())
            with tempfile.TemporaryDirectory() as tmpdirname:
                temp_dir = f"{os.path.abspath(tmpdirname)}"
                output_path = download(url, temp_dir)
                assert os.path.exists(output_path)
