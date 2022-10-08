import requests
from sys import platform


def url_to_name(url):
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
    return f"{name}.html"


def system_checker(url, output):
    if platform in ("linux", "linux2", "darwin"):
        return f"{output}" + url_to_name(url)
    if output.endswith('\\'):
        return f"{output}{url_to_name(url)}"
    else:
        return f"{output}\\{url_to_name(url)}"


def download(url, output):
    new_output = system_checker(url, output)
    response = requests.get(url)
    with open(new_output, 'w', encoding="utf-8") as f:
        f.write(response.text)
    return new_output


# print(download('https://ru.hexlet.io/courses', 'tests\\fixtures\\'))
# print(download('https://ru.hexlet.io/courses'))
