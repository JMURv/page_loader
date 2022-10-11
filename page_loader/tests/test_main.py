import pytest
import os
import tempfile
import requests_mock
from page_loader.naming_generators import url2name
from page_loader import download


def get_fixture_path(name):
    return os.path.join('page_loader', 'tests', 'fixtures', name)


@pytest.mark.parametrize(
    ("url", "result"),
    [
        (
            "https://ru.hexlet.io/courses",
            'ru-hexlet-io-courses'
        ),
        (
            "http://ent-services.ru",
            "ent-services-ru"
        ),
        (
            "https://github.com/JMURv/",
            "github-com-JMURv"
        )
    ]
)
def test_correct_name(url, result):
    assert url2name(url) == result


@pytest.mark.parametrize(
    ("url", "fixture_path"),
    [
        (
            "https://ru.hexlet.io/courses",
            'ru-hexlet-io-courses_no_load.html'
        ),
    ]
)
def test_download_no_load(url, fixture_path):
    fixture_path = get_fixture_path(fixture_path)
    with requests_mock.Mocker() as m:
        with open(fixture_path, 'r', encoding='UTF8') as f:
            m.get(url, text=f.read())
            with tempfile.TemporaryDirectory() as tmpdirname:
                temp_dir = f"{os.path.abspath(tmpdirname)}"
                output_path = download(url, temp_dir)
                assert os.path.exists(output_path)


@pytest.mark.parametrize(
    ("url", "fixture_path"),
    [
        (
            "https://ru.hexlet.io/courses",
            'ru-hexlet-io-courses_no_load.html'
        ),
    ]
)
def test_download_img(url, fixture_path):
    fixture_path = get_fixture_path(fixture_path)
    with requests_mock.Mocker() as m:
        with open(fixture_path, 'r', encoding='UTF8') as f:
            m.get(url, text=f.read())
            with tempfile.TemporaryDirectory() as tmpdirname:
                temp_dir = f"{os.path.abspath(tmpdirname)}"
                download(url, temp_dir)
                directory_path = os.path.join(temp_dir, 'ru-hexlet-io-courses_files')
                file_path = os.path.join(
                    temp_dir,
                    'ru-hexlet-io-courses_files',
                    'at_a_laptop-8c6e59267f91a6bf13bae0e5c0f7e1f36accc440b8d760bca08ab244e2b8bdbf.png'
                )
                assert os.path.exists(directory_path)
                assert os.path.exists(file_path)
