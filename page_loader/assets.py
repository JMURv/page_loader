import os
import requests as req
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from page_loader.url import generate_assets_path, create_filename
import logging
from progress.bar import Bar


ASSETS = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}


def download_assets(for_down, output):
    if not os.path.exists(output):  # Check if dir already exists
        logging.info(
            f"Directory not exists: {output}")
        os.makedirs(output)
    bar = Bar('Loading', fill='|', suffix='%(percent)d%%', max=len(for_down))
    for asset in for_down:
        bar.next()
        filename, link = asset  # Get info from array
        out = os.path.join(output, filename)  # Create right output path
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
    response = req.get(url)  # Get response
    response.raise_for_status()  # Check if resp is success
    for_download = []  # Array with assets info as name and link
    soup = bs(response.content, 'html.parser')
    for asset in ASSETS.keys():
        attr = ASSETS[asset]  # Get right attr
        for link in soup.find_all(asset):
            if link.attrs.get(attr) and is_valid_asset(url, link[attr]):
                down_link = urljoin(url, link[attr])
                filename = create_filename(down_link)
                for_download.append((filename, down_link))
                new_link_name = generate_assets_path(url, link[attr])
                link[attr] = link[attr].replace(link[attr], new_link_name)
    return soup.prettify(), for_download
