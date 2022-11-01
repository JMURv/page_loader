import pytest
import os
import requests_mock
from page_loader import download


def read_content(filepath, mode):
    with open(filepath, mode, encoding='UTF8') as file:
        return file.read()


def get_fixture_path(name):
    return os.path.join(
        'tests', 'fixtures', 'local', name
    )


def get_assets_path(name):
    return os.path.join(
        'tests', 'fixtures', 'local', 'assets', name
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
def test_download_assets(tmpdir, test_url, fixture_path):
    fixture_path = get_fixture_path(fixture_path)
    temp_dir = f"{os.path.abspath(tmpdir)}"
    with requests_mock.Mocker() as m:
        f = read_content(fixture_path, 'r')
        for path, url in TEST_ASSETS:
            with open(path, "rb") as asset_path:
                m.get(url, content=asset_path.read())
        m.get(test_url, text=f, status_code=200)
        output_path = download(test_url, temp_dir)
        result = read_content(output_path, 'r')
        expected = read_content(get_fixture_path('expected_result.html'), 'r')
        files_path = os.path.join(temp_dir, 'my-site-ru_files')
        assert os.path.exists(output_path)
        assert os.path.exists(files_path)
        assert len(os.listdir(temp_dir)) == 2
        assert len(os.listdir(files_path)) == 3
        assert result == expected
