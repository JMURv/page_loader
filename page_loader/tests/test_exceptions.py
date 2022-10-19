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
        assert error.value.args[0] == 'Status code error: 404'


# def test_download_assets():
#     for_down = [('test.png', 'https://my_site.ru/assets/test.png')]
#     link = for_down[0][1]
#     output = 'assets/local'
#     with requests_mock.Mocker() as m:
#         m.get(link, status_code=404)
#         with pytest.raises(Exception) as error:
#             parsing.download_assets(for_down, output)
#         assert error.value.args[0] == f"Resource {link} wasn't downloaded"
