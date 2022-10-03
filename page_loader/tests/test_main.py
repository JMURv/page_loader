from page_loader import download
import requests
import requests_mock


def test_correct_name():
    file_path = download('https://ru.hexlet.io/courses', 'tests/fixtures/')
    assert file_path == 'tests/fixtures/ru-hexlet-io-courses.html'

