from urllib.parse import urlparse
from urllib.parse import urljoin


def url2name(url):
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
    return name.strip('-')


def local_path(link, site_name, url):
    list_of_path = link.split('/')
    filename = list_of_path[-1]
    new_url = urljoin(url, link)
    name_index = new_url.rfind('/')
    if '.' in list_of_path[-1]:
        return f"{site_name}_files/{url2name(new_url[:name_index])}-{filename}"
    return f"{site_name}_files/{url2name(new_url[:name_index])}-{filename}.html"


def http_path(link, site_name, url):
    link_domain = urlparse(link).netloc
    original_domain = urlparse(url).netloc
    if link_domain == original_domain:
        filename = link.split('/')[-1]
        if '.' in filename:
            index = link[::-1].index("/")
            out_link = f"{url2name(link[:-index-1])}-{filename}"
            return f"{site_name}_files/{out_link}"
        else:
            return f"{site_name}_files/{site_name}.html"
    return link


def generate_assets_path(link, site_name, url):
    if link.lower().startswith("https") or link.lower().startswith("http"):
        return http_path(link, site_name, url)
    return local_path(link, site_name, url)


# print(generate_assets_path(
# '/about/rss.css', 'ru-hexlet-io-courses', 'https://ru.hexlet.io/courses'
# ))
# print(generate_assets_path(
# '/about/contacts', 'ru-hexlet-io-courses', 'https://ru.hexlet.io/courses'
# ))
# print(generate_assets_path(
# 'https://cdn2-site.ru', 'ru-hexlet-io-courses', 'https://ru.hexlet.io/courses'
# ))
# print(generate_assets_path(
# 'http://my-site.ru/assets/scripts.js', 'my-site-ru', 'https://my-site.ru'
# ))
