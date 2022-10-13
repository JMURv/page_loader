import os
from page_loader.parsing import prepare_assets
from page_loader.naming_generators import url2name
import logging
from urllib.parse import urlparse


def download(url, output):
    logging.basicConfig(level='INFO')
    logger = logging.getLogger()
    logger.info(f'Requested url : {url}')
    # Generating all the names we'll need
    site_name = url2name(url)
    html_out = os.path.join(output, f"{site_name}.html")
    logger.info(f'Writing file to: {html_out}')
    dir_name = f"{site_name}_files"
    # Process of parsing and writing results to the file
    prepare_assets(url, site_name, html_out, output)
    # prepare_assets(url, site_name, html_out, f"{os.path.join(output, dir_name)}")
    return html_out


# print(download('https://ru.hexlet.io/courses', 'tests\\fixtures\\'))
# print(download('https://ru.hexlet.io/courses', 'tests\\fixtures\\'))
# print(download('https://ru.hexlet.io/courses'))
