import os
import requests as req
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from page_loader.url import generate_assets_path, create_filename, to_dir_path
import logging
from progress.bar import Bar


ASSETS = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}


def download_assets(for_down, output, url):
    dir_output = f"{os.path.join(output, to_dir_path(url))}"
    if not os.path.exists(dir_output):
        logging.info(
            f"Directory not exists: {dir_output}")
        os.makedirs(dir_output)
    bar = Bar('Loading', fill='|', suffix='%(percent)d%%', max=len(for_down))
    for asset in for_down:
        bar.next()
        filename, link = asset
        out = os.path.join(dir_output, filename)
        try:
            r = req.get(link)
            with open(out, 'wb') as f:
                f.write(r.content)
        except Exception as ex:
            cause_info = (ex.__class__, ex, ex.__traceback__)
            logging.debug(str(ex), exc_info=cause_info)
            logging.warning(f"Resource {link} wasn't downloaded")
    bar.finish()


def is_valid_asset(url, link):
    if link.startswith(('http://', 'https://')):
        return True if urlparse(link).netloc == urlparse(url).netloc else False
    return True


def prepare_assets(url):
    response = req.get(url)
    response.raise_for_status()
    for_download = []
    soup = bs(response.content, 'html.parser')
    for asset in ASSETS.keys():
        attr = ASSETS[asset]
        for link in soup.find_all(asset):
            if link.attrs.get(attr) and is_valid_asset(url, link[attr]):
                down_link = urljoin(url, link[attr])
                filename = create_filename(down_link)
                for_download.append((filename, down_link))
                new_link_name = generate_assets_path(url, link[attr])
                link[attr] = link[attr].replace(link[attr], new_link_name)
    return soup.prettify(), for_download
