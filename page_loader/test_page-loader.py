import pytest
import os
import tempfile
import requests_mock
from page_loader import download


def get_fixture_path(name):
    return os.path.join(
        'page_loader', 'tests', 'fixtures', 'local', name
    )


def get_assets_path(name):
    return os.path.join(
        'page_loader', 'tests', 'fixtures', 'local', 'assets', name
    )


TEST_ASSETS = [
    (get_assets_path('my_img.png'), 'https://my-site.ru/assets/my_img.png'),
    (get_assets_path('my_css.css'), 'https://my-site.ru/assets/my_css.css'),
    (get_assets_path('my_script.js'), 'https://my-site.ru/assets/my_script.js')
]


@pytest.mark.parametrize(
    ("test_url", "fixture_path"),
    [
        (
            "https://my-site.ru",
            "my_site.html"
        ),
    ]
)
def test_download_assets(test_url, fixture_path):
    fixture_path = get_fixture_path(fixture_path)
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_dir = f"{os.path.abspath(tmpdirname)}"
        with requests_mock.Mocker() as m:
            with open(fixture_path, 'r', encoding='UTF8') as f:
                for path, url in TEST_ASSETS:
                    with open(path, "rb") as asset_path:
                        m.get(url, content=asset_path.read())
                m.get(test_url, text=f.read(), status_code=200)
                output_path = download(test_url, temp_dir)
                files_path = os.path.join(temp_dir, 'my-site-ru_files')
                assert os.path.exists(output_path)
                assert os.path.exists(files_path)
                assert len(os.listdir(temp_dir)) == 2
                assert len(os.listdir(files_path)) == 3


# @pytest.mark.parametrize(
#     ("url", "fixture_path"),
#     [
#         (
#             "https://my-site.ru",
#             "my_site.html"
#         ),
#     ]
# )
# def test_download(url, fixture_path):
#     fixture_path = get_fixture_path(fixture_path)
#     with tempfile.TemporaryDirectory() as tmpdirname:
#         temp_dir = f"{os.path.abspath(tmpdirname)}"
#         with requests_mock.Mocker() as m:
#             with open(fixture_path, 'r', encoding='UTF8') as f:
#                 # mock img
#                 img = open(get_assets_path('my_img.png'), 'rb').read()
#                 m.get('https://my-site.ru/assets/my_img.png', content=img)
#
#                 # mock CSS
#                 css = open(get_assets_path('my_css.css'), 'rb').read()
#                 m.get('https://my-site.ru/assets/my_css.css', content=css)
#
#                 # mock Script
#                 script = open(get_assets_path('my_script.js'), 'rb').read()
#                 m.get(
#                 'https://my-site.ru/assets/my_script.js', content=script)
#
#                 # mock Site
#                 m.get(url, text=f.read(), status_code=200)
#
#                 output_path = download(url, temp_dir)
#                 result = open(output_path, 'r', encoding='UTF-8').read()
#                 expected = open(
#                     get_fixture_path('expected_result.html'),
#                     'r', encoding='UTF-8').read()
#
#                 files_path = os.path.join(temp_dir, 'my-site-ru_files')
#                 assert os.path.exists(output_path)
#                 assert os.path.exists(files_path)
#                 assert len(os.listdir(temp_dir)) == 2
#                 assert len(os.listdir(files_path)) == 3
#                 assert result == expected
