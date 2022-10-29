import pytest
from page_loader.url import generate_html_path
from page_loader.url import url2name, create_filename


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
    ("url", "link", "result"),
    [
        (
            'https://ru.hexlet.io/courses',
            'https://ru.hexlet.io/packs/js/runtime.js',
            'ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js'
        ),
        (
            'https://ru.hexlet.io/courses',
            '/courses',
            'ru-hexlet-io-courses_files/courses.html'
        ),
        (
            'https://ru.hexlet.io/courses',
            '/assets/application.css',
            'ru-hexlet-io-courses_files/assets-application.css'
        ),
    ]
)
def test_naming(url, link, result):
    output = generate_html_path(url, link)
    assert output == result


@pytest.mark.parametrize(
    ("link", "expected"),
    [
        (
            'https://ru.hexlet.io/packs/js/runtime.js',
            'ru-hexlet-io-packs-js-runtime.js'
        ),
        (
            'https://cdn2.hexlet.io/assets/menu.css',
            'cdn2-hexlet-io-assets-menu.css'
        ),
        (
            '/courses',
            'courses.html'
        ),
        (
            '/assets/application.css',
            'assets-application.css'
        ),
        (
            'assets/application.png?test',
            'assets-application.png'
        )
    ]
)
def test_create_filename(link, expected):
    assert create_filename(link) == expected
