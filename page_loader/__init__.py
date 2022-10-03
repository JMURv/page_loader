import requests


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


def download(url, output):
    new_output = output + url_to_name(url)
    response = requests.get(url)
    with open(new_output, 'w', encoding="utf-8") as f:
        f.write(response.text)
    return new_output


# print(download('https://ru.hexlet.io/courses', 'tests/fixtures/'))
# print(download('https://ru.hexlet.io/courses'))