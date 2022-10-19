from urllib.parse import urlparse


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
    if name[-1] == '-':
        name = name[:-1]
    return name


def local_path(link, site_name, url):
    list_of_path = link.split('/')
    filename = '-'.join(list_of_path)
    if '.' in list_of_path[-1]:
        return f"{site_name}_files/{url2name(urlparse(url).netloc)}{filename}"
    return f"{site_name}_files/{url2name(urlparse(url).netloc)}{filename}.html"


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
    if link.lower().startswith("https"):
        return http_path(link, site_name, url)
    return local_path(link, site_name, url)
