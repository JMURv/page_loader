from bs4 import BeautifulSoup as bs
import os
import requests as req
from urllib.request import urlretrieve, urlopen
from urllib.parse import urljoin
from page_loader.naming_generators import generate_assets_name
import shutil


# def download_img(url, site_name, html_out, output):
#     # Open newly generated file
#     with open(html_out, encoding='UTF8') as f:
#         file = f.read()
#     soup = bs(file, 'html.parser')
#     for link in soup.findAll("img"):
#         filename = link["src"].split("/")[-1]
#         outpath = os.path.join(output, filename)
#         # Checking if asset has a http or local path
#         if link["src"].lower().startswith("https"):
#             urlretrieve(link["src"], outpath)
#             new_link_name = generate_assets_name(link["src"], site_name)
#             print(new_link_name)
#             link['src'] = link['src'].replace(link['src'], new_link_name)
#         else:
#             # Get right URL
#             join_urls = urljoin(url, link['src'])
#             img_data = req.get(join_urls).content
#             # Changing the 'src' parameter to the user local path
#             new_link_name = generate_assets_name(link["src"], site_name)
#             print(new_link_name)
#             link['src'] = link['src'].replace(link['src'], new_link_name)
#             # Write file
#             with open(outpath, 'wb') as f:
#                 f.write(img_data)
#     # Rewrite the HTML DOM
#     with open(html_out, "wb") as f_output:
#         f_output.write(soup.prettify("utf-8"))


def download_img(url, site_name, html_out, output):
    # Open newly generated file
    with open(html_out, encoding='UTF8') as f:
        file = f.read()
    soup = bs(file, 'html.parser')
    assets = ['img', 'link', 'script']
    for asset in assets:
        if asset in ('img', 'script'):
            attr = 'src'
        else:
            attr = 'href'
        for link in soup.findAll(asset):
            try:
                link[attr]
            except Exception:
                break
            filename = link[attr].split("/")[-1]
            outpath = os.path.join(output, filename)
            # Checking if asset has a http or local path
            if link[attr].lower().startswith("https"):
                print(link[attr])
                join_urls = urljoin(url, link[attr])
                urlretrieve(join_urls, outpath)
                new_link_name = generate_assets_name(link[attr], site_name)
                link[attr] = link[attr].replace(link[attr], new_link_name)
        # Rewrite the HTML DOM
        with open(html_out, "wb") as f_output:
            f_output.write(soup.prettify("utf-8"))


# print(dowload_other_assets(
#     'https://ru.hexlet.io/courses',
#     'ru-hexlet-io-courses',
#     'C:\\Users\\DOROTHY\\PycharmProjects\\pythonProject-51\\page_loader\\tests\\fixtures\\local\\simple_fixture.html',
#     'tests/fixtures/loclal/assets'))