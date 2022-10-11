import requests
import os
from page_loader.parsing import download_img


def url_to_name(url, output):
    name = ''
    if url.startswith('http://'):
        url = url[7:]
    elif url.startswith('https://'):
        url = url[8:]
    for char in url:
        if char.isalnum():
            name += char
        else:
            name += '-'
    if name[-1] == '-':
        name = name[:-1]
    return os.path.join(output, f"{name}.html"), f"{name}_files"


def makedr(out, dirname):
    newpath = f'{os.path.join(os.getcwd(), out, dirname)}'
    if not os.path.exists(newpath):
        os.makedirs(newpath)


def download(url, output):
    file_out, dir_name = url_to_name(url, output)
    response = requests.get(url)
    with open(file_out, 'w', encoding="utf-8") as f:
        f.write(response.text)
    makedr(output, dir_name)
    download_img(file_out, f"{os.path.join(output, dir_name)}")
    return file_out


# print(download('https://ru.hexlet.io/courses', 'tests\\fixtures\\'))
# print(download('https://ru.hexlet.io/courses'))
