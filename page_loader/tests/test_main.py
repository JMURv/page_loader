import pytest
import os
import tempfile
import requests_mock
from page_loader import url_to_name
from page_loader import download


def get_fixture_path(name):
    return os.path.join('page_loader', 'tests', 'fixtures', name)


@pytest.mark.parametrize(
    ("url", "result"),
    [
        (
            "https://ru.hexlet.io/courses",
            'ru-hexlet-io-courses.html'
        ),
        (
            "http://ent-services.ru",
            "ent-services-ru.html"
        ),
        (
            "https://github.com/JMURv/",
            "github-com-JMURv.html"
        )
    ]
)
def test_correct_name(url, result):
    assert url_to_name(url) == result


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
