import requests
import os
from page_loader.parsing import download_img
from page_loader.naming_generators import url2name


def makedr(output, dirname):
    newpath = f'{os.path.join(os.getcwd(), output, dirname)}'
    if not os.path.exists(newpath):
        os.makedirs(newpath)


def download(url, output):
    # Generate all the names I need
    name = url2name(url)
    file_out = os.path.join(output, f"{name}.html")
    dir_name = f"{name}_files"
    # Process of parsing and writing results to the file
    response = requests.get(url)
    with open(file_out, 'w', encoding="utf-8") as f:
        f.write(response.text)
        makedr(output, dir_name)
        download_img(url, name, file_out, f"{os.path.join(output, dir_name)}")
    return file_out


# print(download('https://ru.hexlet.io/courses', 'tests\\fixtures\\'))
# print(download('https://ru.hexlet.io/courses'))
