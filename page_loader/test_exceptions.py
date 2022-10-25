import pytest
from page_loader import assets


def test_prepare_assets():
    url = 'https://my_site.ru'
    site_name = 'my-site-ru'
    with pytest.raises(Exception):
        assets.prepare_assets(url, site_name)

