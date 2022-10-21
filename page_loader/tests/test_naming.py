import pytest
from page_loader.naming_generators import generate_assets_path
from page_loader.naming_generators import url2name
from page_loader.parsing import validator_assets


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


@pytest.mark.parametrize(
    ("url", "link", 'expected'),
    [
        (
            'https://hexlet.io/courses',
            '/about/rss.css',
            ('hexlet-io-about-rss.css', 'https://hexlet.io/about/rss.css')
        ),
        (
            'https://hexlet.io/courses',
            '/about/contacts',
            ('hexlet-io-about-contacts.html',
             'https://hexlet.io/about/contacts')
        ),
        (
            'https://hexlet.io/courses',
            'https://cdn2-site.ru',
            ('0', 'https://cdn2-site.ru')
        ),
    ]
)
def test_assets_validator(url, link, expected):
    result = validator_assets(url, link)
    assert result == expected
