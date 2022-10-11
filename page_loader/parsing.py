from bs4 import BeautifulSoup
import os
from urllib.request import urlretrieve


def download_img(path, output):
    with open(path, encoding='UTF8') as f:
        file = f.read()
    soup = BeautifulSoup(file, 'html.parser')
    for link in soup.select("img[src]"):
        filename = link["src"].split("/")[-1]
        outpath = os.path.join(output, filename)
        urlretrieve(link["src"], outpath)
        new_link_name = output.split('\\')[-1] + '/' + path.split('\\')[-1][:-5] + '-assets-' + filename
        link['src'] = link['src'].replace(link['src'], new_link_name)
    with open(path, "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))
