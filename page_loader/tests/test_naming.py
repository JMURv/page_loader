import pytest
from page_loader.naming_generators import generate_http_assets_name, generate_local_assets_name


@pytest.mark.parametrize(
    ("fixture", "site_name", "url", "result"),
    [
        (
            '/assets/application.css',
            'ru-hexlet-io-courses',
            'https://ru.hexlet.io/courses',
            'ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css'
        ),
        (
            '/courses',
            'ru-hexlet-io-courses',
            'https://ru.hexlet.io/courses',
            'ru-hexlet-io-courses_files/ru-hexlet-io-courses.html'
        )
    ]
)
def test_local_naming(site_name, url, fixture, result):
    output = generate_local_assets_name(fixture, site_name, url)
    assert output == result


@pytest.mark.parametrize(
    ("fixture", "site_name", "url", "result"),
    [
        (
            'https://ru.hexlet.io/packs/js/runtime.js',
            'ru-hexlet-io-courses',
            'https://ru.hexlet.io/courses',
            'ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js'
        ),
        (
            'https://cdn2.hexlet.io/assets/menu.css',
            'ru-hexlet-io-courses',
            'https://ru.hexlet.io/courses',
            'https://cdn2.hexlet.io/assets/menu.css'
        )
    ]
)
def test_http_naming(site_name, url, fixture, result):
    output = generate_http_assets_name(fixture, site_name, url)
    assert output == result
