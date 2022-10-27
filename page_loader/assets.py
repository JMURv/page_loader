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
        filename, link = asset[0], asset[1]  # Get info from array
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


def validator_assets(url, link):
    down_link = link[:]  # Copy link
    if not down_link.startswith(('https://', 'http://')):
        down_link = urljoin(url, link)  # Create download link
    if urlparse(down_link).netloc == urlparse(url).netloc:  # If link is local
        filename = create_filename(down_link)
        return filename, down_link  # Successful return of local link and name
    return '0', down_link  # Return non-local as zero


def is_valid_asset(url, link):
    down_link = urljoin(url, link)  # Create download link
    return True if urlparse(down_link).netloc == urlparse(url).netloc else False


def prepare_assets(url):
    response = req.get(url)  # Get response
    response.raise_for_status()  # Check if resp is success
    for_download = []  # Array with assets info as name and link
    soup = bs(response.content, 'html.parser')
    for asset in ASSETS.keys():
        attr = ASSETS[asset]  # Get right attr
        for link in soup.find_all(asset):
            if link.attrs.get(attr) and is_valid_asset(url, link[attr]):
                filename, down_link = validator_assets(url, link[attr])
                for_download.append((filename, down_link))
                # Generate new paths for HTML file
                new_link_name = generate_assets_path(url, link[attr])
                # Replace paths with newly generated
                link[attr] = link[attr].replace(link[attr], new_link_name)
    return soup.prettify(), for_download
