from urllib.parse import urljoin, urlparse
import re
import os


def url2name(url):
    parsed = urlparse(url.strip('/'))
    url = f"{parsed.netloc}{parsed.path}"
    reg_exp = re.compile(r"[^a-zA-Z\d+]")
    result = reg_exp.sub('-', url)
    return result.strip('-')


def local_path(url, link):
    new_url = urljoin(url, link)
    path, extension = os.path.splitext(new_url)
    name_index = new_url.rfind('/')
    if '.' in extension:
        return f"{url2name(url)}_files/{url2name(path)}{extension}"
    return f"{url2name(url)}_files/{url2name(path)}-{extension}.html"

# print(local_path('https://ru.hexlet.io/courses', 'aboba/files/my_css.css'))


def http_path(url, link):
    link_domain = urlparse(link).netloc
    original_domain = urlparse(url).netloc
    site_name = url2name(url)
    if link_domain == original_domain:
        filename = link.split('/')[-1]
        if '.' in filename:
            index = link.rfind("/")
            out_link = f"{url2name(link[:index])}-{filename}"
            return f"{site_name}_files/{out_link}"
        else:
            return f"{site_name}_files/{site_name}.html"
    return link


def generate_assets_path(url, link):
    if link.startswith(('http', 'https')):
        return http_path(url, link)
    else:
        return local_path(url, link)


def create_filename(link):
    filename = link.split('/')[-1]  # Extract filename from link
    rename_link = url2name(link[:link.rfind('/')])
    filename = f"{rename_link}-{filename}"  # Rename filename by full path
    if '.' not in filename:
        filename = f"{url2name(link)}.html"
    if '?' in filename:  # Check for GET request in filename
        index = filename.rfind('?')
        filename = filename[:index]
    return filename
