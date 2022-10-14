import pytest
from page_loader.naming_generators import generate_assets_path


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
        ),
        (
            '/courses',
            'ru-hexlet-io-courses',
            'https://ru.hexlet.io/courses',
            'ru-hexlet-io-courses_files/ru-hexlet-io-courses.html'
        ),
        (
            '/assets/application.css',
            'ru-hexlet-io-courses',
            'https://ru.hexlet.io/courses',
            'ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css'
        ),
    ]
)
def test_naming(site_name, url, fixture, result):
    output = generate_assets_path(fixture, site_name, url)
    assert output == result
