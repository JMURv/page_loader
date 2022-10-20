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


@pytest.mark.parametrize(
    ("url", "fixture_path"),
    [
        (
            "https://my-site.ru",
            "my_site.html"
        ),
    ]
)
def test_download(url, fixture_path):
    fixture_path = get_fixture_path(fixture_path)
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_dir = f"{os.path.abspath(tmpdirname)}"
        with requests_mock.Mocker() as m:
            with open(fixture_path, 'r', encoding='UTF8') as f:
                # mock img
                img = open(get_assets_path('my_img.png'), 'rb').read()
                m.get('https://my-site.ru/assets/my_img.png', content=img)

                # mock CSS
                css = open(get_assets_path('my_css.css'), 'rb').read()
                m.get('https://my-site.ru/assets/my_css.css', content=css)

                # mock Script
                script = open(get_assets_path('my_script.js'), 'rb').read()
                m.get('https://my-site.ru/assets/my_script.js', content=script)

                # mock Site
                m.get(url, text=f.read())

                output_path = download(url, temp_dir)
                result = open(output_path, 'r', encoding='UTF-8').read()
                expected = open(
                    get_fixture_path('expected_result.html'),
                    'r', encoding='UTF-8').read()

                files_path = os.path.join(temp_dir, 'my-site-ru_files')
                assert os.path.exists(output_path)
                assert os.path.exists(files_path)
                assert len(os.listdir(temp_dir)) == 2
                assert len(os.listdir(files_path)) == 3
                assert result == expected


def get_fixture_path_hex(name):
    return os.path.join(
        'page_loader', 'tests', 'fixtures', name
    )


def get_assets_path_hex(name):
    return os.path.join(
        'page_loader', 'tests', 'fixtures', 'expected', 'localhost-blog-about_files', name
    )


@pytest.mark.parametrize(
    ("url", "fixture_path"),
    [
        (
            "https://my-site.ru",
            "localhost-blog-about.html"
        ),
    ]
)
def test_download(url, fixture_path):
    fixture_path = get_fixture_path_hex(fixture_path)
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_dir = f"{os.path.abspath(tmpdirname)}"
        with requests_mock.Mocker() as m:
            with open(fixture_path, 'r', encoding='UTF8') as f:
                # mock img
                img = open(get_assets_path_hex('localhost-photos-me.jpg'), 'rb').read()
                m.get('https://my-site.ru/photos/me.jpg', content=img)

                # mock CSS
                css = open(get_assets_path_hex('localhost-blog-about-assets-styles.css'), 'rb').read()
                m.get('https://my-site.ru/blog/about/assets/styles.css', content=css)

                # mock Script
                script = open(get_assets_path_hex('localhost-assets-scripts.js'), 'rb').read()
                m.get('http://my-site.ru/assets/scripts.js', content=script)

                # mock HTML
                html_in = open(get_assets_path_hex('localhost-blog-about.html'), 'rb').read()
                m.get('https://my-site.ru/blog/about', content=html_in)

                # mock Site
                m.get(url, text=f.read())
                output_path = download(url, temp_dir)
                files_path = os.path.join(temp_dir, 'my-site-ru_files')
                assert os.path.exists(output_path)
                assert os.path.exists(files_path)
                assert len(os.listdir(temp_dir)) == 2
                assert len(os.listdir(files_path)) == 4
                # assert result == expected
