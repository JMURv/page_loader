import pytest
from page_loader.url import generate_path
from page_loader.url import url2name


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
def test_url2name(url, result):
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
        (
            'https://ru.hexlet.io/courses',
            '/assets/application.css?test_get',
            'ru-hexlet-io-courses_files/assets-application.css'
        ),
    ]
)
def test_generate_path(url, link, result):
    output = generate_path(url, link)
    assert output == result
