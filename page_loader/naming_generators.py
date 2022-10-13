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


def generate_http_assets_name(link, site_name, url):
    link_domain = urlparse(link).netloc
    original_domain = urlparse(url).netloc
    if link_domain == original_domain:
        extension = link.split('.')[-1]
        link = url2name(link)
        link = '-'.join(link.split('-')[:-1])
        return f"{site_name}_files/{link}.{extension}"
    return link


def generate_local_assets_name(link, site_name, url):
    list_of_path = link.split('/')
    filename = '-'.join(list_of_path)
    if '.' in list_of_path[-1]:
        return f"{site_name}_files/{url2name(urlparse(url).netloc)}{filename}"
    return f"{site_name}_files/{url2name(urlparse(url).netloc)}{filename}.html"
