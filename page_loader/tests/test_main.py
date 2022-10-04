# from page_loader import download
from page_loader import url_to_name
# import tempfile
# import requests
# import requests_mock
# import pathlib


def test_correct_name():
    file_path = url_to_name('https://ru.hexlet.io/courses')
    assert file_path == 'ru-hexlet-io-courses.html'


def test_download():
    pass
