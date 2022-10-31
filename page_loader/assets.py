import os
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from page_loader.url import generate_path, to_dir_path
import logging
from progress.bar import Bar


ASSETS = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}


def download_assets(media_files, output_dir, url):
    dir_output = f"{os.path.join(output_dir, to_dir_path(url))}"
    if not os.path.exists(dir_output):
        logging.info(
            f"Directory not exists: {dir_output}")
        os.makedirs(dir_output)
    bar = Bar(
        'Loading', fill='|', suffix='%(percent)d%%', max=len(media_files)
    )
    for asset in media_files:
        bar.next()
        filename, link = asset
        try:
            logging.info('Downloading assets..')
            r = requests.get(link)
            with open(filename, 'wb') as f:
                f.write(r.content)
        except Exception as ex:
            cause_info = (ex.__class__, ex, ex.__traceback__)
            logging.debug(str(ex), exc_info=cause_info)
            logging.warning(f"Resource {link} wasn't downloaded")
    bar.finish()


def is_valid_asset(site_url, asset_url):
    if asset_url.startswith(('http://', 'https://')):
        site_url_netloc = urlparse(site_url).netloc
        asset_url_netloc = urlparse(asset_url).netloc
        return True if asset_url_netloc == site_url_netloc else False
    return True


def prepare_assets(url, output_dir):
    response = requests.get(url)
    response.raise_for_status()
    media_files = []
    soup = bs(response.content, 'html.parser')
    for asset in ASSETS.keys():
        attr = ASSETS[asset]
        for link in soup.find_all(asset):
            if link.attrs.get(attr) and is_valid_asset(url, link[attr]):
                down_link = urljoin(url, link[attr])
                filename = generate_path(url, down_link)
                outpath = os.path.join(output_dir, filename)
                media_files.append((outpath, down_link))
                link[attr] = link[attr].replace(link[attr], filename)
    return soup.prettify(), media_files
