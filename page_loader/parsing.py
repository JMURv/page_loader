import os
import requests as req
from bs4 import BeautifulSoup as bs
from urllib.request import urlretrieve
from urllib.parse import urljoin
from page_loader.naming_generators import generate_http_assets_name, generate_local_assets_name
import logging
from progress.bar import Bar


def makedir(output, dirname):
    newpath = f'{os.path.join(os.getcwd(), output, dirname)}'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath


def download_assets(attr, asset, url, site_name, output):
    try:
        if asset.attrs.get(attr):
            filename = asset[attr].split('/')[-1]
            outpath = os.path.join(output, filename) if '.' in filename else os.path.join(output, f"{filename}.html")
            if asset[attr].lower().startswith("https"):
                urlretrieve(urljoin(url, asset[attr]), outpath)
                new_link_name = generate_http_assets_name(asset[attr], site_name, url)
                asset[attr] = asset[attr].replace(asset[attr], new_link_name)
            else:
                r = req.get(urljoin(url, asset[attr]))
                with open(outpath, 'wb') as f:
                    f.write(r.content)
                new_link_name = generate_local_assets_name(asset[attr], site_name, url)
                asset[attr] = asset[attr].replace(asset[attr], new_link_name)
    except Exception as ex:
        logging.warning(f"Resource {asset[attr]} wasn't downloaded")


def prepare_assets(url, site_name, html_out, output):
    logging.basicConfig(level='INFO')
    logger = logging.getLogger()
    response = req.get(url)
    if response.status_code != 200:  # Checking status code
        raise Warning(f'Status code error: {url.status_code}')
    with open(html_out, 'w', encoding='UTF-8') as f:
        f.write(response.text)  # Save the HTML file
    output = makedir(output, f"{site_name}_files")
    soup = bs(response.content, 'html.parser')
    assets = ['img', 'link', 'script']  # List of assets we need
    bar = Bar('Loading', fill='|', suffix='%(percent)d%%')
    logger.info(f'Downloading assets...')
    for asset in assets:
        attr = 'src' if asset in ('img', 'script') else 'href'  # Get the right attribute
        for link in soup.find_all(asset):
            download_assets(attr, link, url, site_name, output)
            bar.next(10)
    with open(html_out, "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))  # Rewrite HTML file
    bar.finish()
    logger.info(f'Finished!')


# print(download_img(
#     'https://skillbox.ru/',
#     'skillbox-ru',
#     'C:\\Users\\DOROTHY\\PycharmProjects\\pythonProject-51\\page_loader\\tests\\fixtures\\local\\simple_fixture.html',
#     'tests\\fixtures\\local\\assets'))

# print(prepare_assets(
#     'https://ru.hexlet.io/courses',
#     'ru-hexlet-io-courses',
#     'C:\\Users\\DOROTHY\\PycharmProjects\\pythonProject-51\\page_loader\\tests\\fixtures\\local\\simple_fixture.html',
# 'tests\\fixtures\\local\\assets'
# ))
