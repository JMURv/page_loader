import os
import requests as req
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from page_loader.naming_generators import generate_assets_path
import logging
from progress.bar import Bar
from page_loader.naming_generators import url2name

DIGITS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']


def makedir(output, dirname):
    newpath = f'{os.path.join(os.getcwd(), output, dirname)}'
    if not os.path.exists(newpath):  # Check if dir already exists
        logging.info(
            f"directory not exists: {newpath}")
        os.makedirs(newpath)
    return newpath


def download_assets(for_down, output):
    bar = Bar('Loading', fill='|', suffix='%(percent)d%%', max=len(for_down))
    for asset in for_down:
        bar.next()
        filename, link = asset[0], asset[1]
        out = os.path.join(output, filename)
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
    if not link.startswith('https://') or 'http://':
        link = urljoin(url, link)
    if urlparse(link).netloc == urlparse(url).netloc:
        filename = link.split('/')[-1]
        rename_index = link.rfind('/')
        rename_link = url2name(link[:rename_index].strip())
        filename = f"{rename_link}-{filename}"
        filename = filename if '.' in filename else f"{url2name(link)}.html"
        if '?' in filename:
            index = filename.rfind('?')
            filename = filename[:index]
        return filename, link
    else:
        return '0', '0'


def prepare_assets(url, site_name):
    response = req.get(url)
    if response.status_code != 200:
        raise Warning(f'Status code error: {response.status_code}')
    for_download = []
    soup = bs(response.content, 'html.parser')
    assets = ['img', 'link', 'script']
    for asset in assets:
        attr = 'src' if asset in ('img', 'script') else 'href'
        for link in soup.find_all(asset):
            if link.attrs.get(attr):
                filename, link[attr] = validator_assets(url, link[attr])
                if filename == '0' or link[attr] == '0':
                    continue
                for_download.append((filename, link[attr]))
                new_link_name = generate_assets_path(link[attr], site_name, url)
                link[attr] = link[attr].replace(link[attr], new_link_name)
    return soup.prettify(), for_download
