import pytest
import requests
from page_loader import assets
from page_loader import download


def test_prepare_assets():
    url = 'https://my_site.ru'
    site_name = 'my-site-ru'
    with pytest.raises(Exception):
        assets.prepare_assets(url, site_name)


def test_no_dir():
    with pytest.raises(FileNotFoundError):
        download('https://ru.hexlet.io/courses', 'testdir\\testdir2')


def test_http_response():
    with pytest.raises(requests.exceptions.HTTPError):
        download('https://ru.hexlet.io/error/response', 'tests/fixtures')
