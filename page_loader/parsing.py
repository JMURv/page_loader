import os
import requests as req
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from page_loader.naming_generators import generate_assets_path
import logging
from progress.bar import Bar
from page_loader.naming_generators import url2name


def makedir(output, dirname):
    newpath = f'{os.path.join(os.getcwd(), output, dirname)}'
    if not os.path.exists(newpath):  # Check if dir already exists
        os.makedirs(newpath)
    return newpath


def download_assets(url, for_down, output):
    bar = Bar('Loading', fill='|', suffix='%(percent)d%%', max=len(for_down))
    for asset in for_down:
        bar.next()
        filename, link = asset[0], asset[1]
        out = os.path.join(output, filename)
        try:
            r = req.get(urljoin(url[:-1], link))
            # r = req.get(link)
            with open(out, 'wb') as f:
                f.write(r.content)
        except Exception as ex:
            cause_info = (ex.__class__, ex, ex.__traceback__)
            logging.debug(str(ex), exc_info=cause_info)
            logging.warning(f"Resource {link} wasn't downloaded")
    bar.finish()


def prepare_assets(url, site_name):
    response = req.get(url)
    if response.status_code != 200:
        raise Warning(f'Status code error: {url.status_code}')
    for_download = []
    soup = bs(response.content, 'html.parser')
    assets = ['img', 'link', 'script']
    for asset in assets:
        attr = 'src' if asset in ('img', 'script') else 'href'
        for link in soup.find_all(asset):
            if link.attrs.get(attr):
                filename = link[attr].split('/')[-1]
                filename = filename if '.' in filename \
                    else f"{url2name(link[attr])}.html"
                if not link[attr].startswith('https://'):
                    link[attr] = urljoin(url, link[attr])
                # print(filename, link[attr])
                for_download.append((filename, link[attr]))
                new_link_name = generate_assets_path(link[attr], site_name, url)
                link[attr] = link[attr].replace(link[attr], new_link_name)
    return soup.prettify(), for_download


# print(prepare_assets(
#     'https://skillbox.ru/',
#     'skillbox-ru'))

# print(prepare_assets(
#     'https://ru.hexlet.io/courses',
#     'ru-hexlet-io-courses'))
