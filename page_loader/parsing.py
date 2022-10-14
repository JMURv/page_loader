import os
import requests as req
from bs4 import BeautifulSoup as bs
from urllib.request import urlretrieve
from urllib.parse import urljoin
from page_loader.naming_generators import generate_assets_path
import logging
from progress.bar import Bar


def makedir(output, dirname):
    newpath = f'{os.path.join(os.getcwd(), output, dirname)}'
    if not os.path.exists(newpath):  # Check if dir already exists
        os.makedirs(newpath)
    return newpath


def download_assets(attr, asset, url, site_name, output):
    if asset.attrs.get(attr):
        filename = asset[attr].split('/')[-1]
        filename = filename if '.' in filename else f"{filename}.html"
        output = os.path.join(output, filename)
        try:
            r = req.get(url).content
            with open(output, 'wb') as f:
                f.write(r)
            new_link_name = generate_assets_path(asset[attr], site_name, url)
            asset[attr] = asset[attr].replace(asset[attr], new_link_name)
        except Exception:
            logging.warning(f"Resource {asset[attr]} wasn't downloaded")


def prepare_assets(url, site_name, html_out, output):
    logging.basicConfig(level='INFO')
    logger = logging.getLogger()
    response = req.get(url)  # Get response
    bar = Bar('Loading', fill='|', suffix='%(percent)d%%')  # This is progress bar!
    if response.status_code != 200:  # Checking status code
        raise Warning(f'Status code error: {url.status_code}')
    with open(html_out, 'w', encoding='UTF-8') as f:
        f.write(response.text)  # Save the HTML file
    output = makedir(output, f"{site_name}_files")  # Reroute output to the new dir
    soup = bs(response.content, 'html.parser')  # Create soup obj
    assets = ['img', 'link', 'script']  # List of assets we need to scrape
    logger.info(f'Downloading assets...')
    for asset in assets:
        attr = 'src' if asset in ('img', 'script') else 'href'  # Get the right attribute for asset
        for link in soup.find_all(asset):
            download_assets(attr, link, url, site_name, output)
            bar.next(10)
    with open(html_out, "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))  # Rewrite HTML file paths
    bar.finish()
    logger.info(f'Finished!')


# print(prepare_assets(
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

# def download_assets(attr, asset, url, site_name, output):
#     if asset.attrs.get(attr):
#         filename = asset[attr].split('/')[-1]  # Get filename from HTML DOM (Probaly an error if name is not found)
#         outpath = os.path.join(output, filename) if '.' in filename else os.path.join(output, f"{filename}.html")  # Check for right extension
#         if asset[attr].lower().startswith("https"):  # If asset has a hyperlink
#             urlretrieve(urljoin(url, asset[attr]), outpath)  # Download asset
#             new_link_name = generate_http_assets_name(asset[attr], site_name, url)  # Generate new path for HTML DOM
#             asset[attr] = asset[attr].replace(asset[attr], new_link_name)  # Apply new path
#         else:
#             r = req.get(urljoin(url, asset[attr]))  # Get the right path for downloading & request
#             with open(outpath, 'wb') as f:
#                 f.write(r.content)  # Download asset
#             new_link_name = generate_local_assets_name(asset[attr], site_name, url)  # Generate new path for HTML DOM
#             asset[attr] = asset[attr].replace(asset[attr], new_link_name)  # Apply new path
#     except Exception as ex:
#         logging.warning(f"Resource {asset[attr]} wasn't downloaded")
