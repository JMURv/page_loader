import pytest
import os
import tempfile
import requests_mock
from page_loader import download


def get_fixture_path(name):
    return os.path.join('page_loader', 'tests', 'fixtures', name)


def get_assets_path(name):
    return os.path.join(
        'page_loader', 'tests', 'fixtures', 'local', 'assets', name
    )


@pytest.mark.parametrize(
    ("url", "fixture_path"),
    [
        (
            "https://my-site.ru",
            "my_site.html"
        ),
    ]
)
def test_existense(url, fixture_path):
    fixture_path = get_fixture_path(fixture_path)
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_dir = f"{os.path.abspath(tmpdirname)}"
        with requests_mock.Mocker() as m:
            with open(fixture_path, 'r', encoding='UTF8') as f:
                # img
                img = open(get_assets_path('my_img.png'), 'rb').read()
                m.get('assets/my_img.png', content=img)

                # CSS
                css = open(get_assets_path('my_css.css'), 'rb').read()
                m.get('assets/my_css.css', content=css)

                # Script
                script = open(get_assets_path('my_script.js'), 'rb').read()
                m.get('assets/my_script.js', content=script)

                # Site
                m.get(url, text=f.read())

                output_path = download(url, temp_dir)
                files_path = os.path.join(temp_dir, 'my-site-ru')
                assert os.path.exists(output_path)
                assert os.path.exists(files_path)
                assert len(os.listdir(temp_dir)) == 2
                assert len(os.listdir(files_path)) == 10


# @pytest.mark.parametrize(
#     ("url", "fixture_path"),
#     [
#         (
#             "https://ru.hexlet.io/courses",
#             'ru-hexlet-io-courses_no_load.html'
#         ),
#     ]
# )
# def test_download_assets(url, fixture_path):
#     fixture_path = get_fixture_path(fixture_path)
#     with requests_mock.Mocker() as m:
#         with open(fixture_path, 'r', encoding='UTF8') as f:
#             m.get(url, text=f.read())
#             with tempfile.TemporaryDirectory() as tmpdirname:
#                 temp_dir = f"{os.path.abspath(tmpdirname)}"
#                 download(url, temp_dir)
#                 directory_path = os.path.join(
#                     temp_dir, 'ru-hexlet-io-courses_files'
#                 )
#                 css_path = os.path.join(
#                     temp_dir,
#                     'ru-hexlet-io-courses_files',
#                     'application-16524c7e.css'
#                 )
#                 assert os.path.exists(directory_path)
#                 assert os.path.exists(css_path)


@pytest.mark.parametrize(
    ("url", "fixture_path"),
    [
        (
            "https://ru.hexlet.io/courses",
            'ru-hexlet-io-courses_no_load.html'
        ),
    ]
)
def test_change_paths(url, fixture_path):
    pass
