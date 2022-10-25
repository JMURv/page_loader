import pytest
import requests_mock
from page_loader import parsing


def test_prepare_assets():
    url = 'https://my_site.ru'
    site_name = 'my-site-ru'
    with requests_mock.Mocker() as m:
        m.get(url, status_code=404)
        with pytest.raises(Exception) as error:
            parsing.prepare_assets(url, site_name)
        assert error.value.args[0] == \
               '404 Client Error: None for url: https://my_site.ru/'
