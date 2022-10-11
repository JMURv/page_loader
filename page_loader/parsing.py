from bs4 import BeautifulSoup as bs
import os
import requests as req
from urllib.request import urlretrieve, urlopen
from urllib.parse import urljoin
from page_loader.naming_generators import generate_assets_name
import shutil


def download_img(url, site_name, path, output):
    # Open newly generated file
    with open(path, encoding='UTF8') as f:
        file = f.read()
    soup = bs(file, 'html.parser')
    for link in soup.findAll("img"):
        filename = link["src"].split("/")[-1]
        outpath = os.path.join(output, filename)
        # Checking if image has a http or local path
        if link["src"].lower().startswith("https"):
            urlretrieve(link["src"], outpath)
        else:
            join_urls = urljoin(url, link['src'])
            # img_data = req.get(join_urls, stream=True).content
            # with open(outpath, 'wb') as f:
            #     img_data.raw.decode_content = True
            #     shutil.copyfileobj(img_data.raw, f)
            img_data = req.get(join_urls).content
            with open(filename, 'wb') as f:
                f.write(img_data)
        # Changing the 'src' parameter to the user local path
        # new_link_name = generate_assets_name(link["src"], site_name)
        # link['src'] = link['src'].replace(link['src'], new_link_name)
    # Rewrite the HTML DOM
    # with open(path, "wb") as f_output:
    #     f_output.write(soup.prettify("utf-8"))

# print(download_img('http://aboba.ru','aboba', r'C:\Users\DOROTHY\PycharmProjects\pythonProject-51\page_loader\tests\fixtures\local\simple_fixture.html', 'tests\\fixtures\\local'))