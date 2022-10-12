import requests
import os
from page_loader.parsing import download_img
# from page_loader.parsing import download_other_assets
from page_loader.naming_generators import url2name


def makedr(output, dirname):
    newpath = f'{os.path.join(os.getcwd(), output, dirname)}'
    if not os.path.exists(newpath):
        os.makedirs(newpath)


def download(url, output):
    # Generating all the names we'll need
    site_name = url2name(url)
    html_out = os.path.join(output, f"{site_name}.html")
    dir_name = f"{site_name}_files"
    # Process of parsing and writing results to the file
    response = requests.get(url)
    with open(html_out, 'w', encoding="utf-8") as f:
        f.write(response.text)
        # Making directory for all the additional files & dowloading the files
        makedr(output, dir_name)
        download_img(url, site_name, html_out, f"{os.path.join(output, dir_name)}")
    return html_out


# print(download('https://ru.hexlet.io/courses', 'tests\\fixtures\\'))
print(download('https://ru.hexlet.io/courses', 'tests\\fixtures\\'))
# print(download('https://ru.hexlet.io/courses'))
