from urllib.parse import urljoin, urlparse
import re
import os


def url2name(url):
    parsed = urlparse(url.strip('/'))
    url = f"{parsed.netloc}{parsed.path}"
    reg_exp = re.compile(r"[^a-zA-Z\d+]")
    result = reg_exp.sub('-', url)
    return result


def generate_assets_path(url, link):
    new_url = urljoin(url, link)
    original_domain = urlparse(url).netloc
    if urlparse(new_url).netloc == original_domain:
        path, extension = os.path.splitext(new_url)
        if '.' in extension:
            return f"{url2name(url)}_files/{url2name(path)}{extension}"
        return f"{url2name(url)}_files/{url2name(path)}{extension}.html"
    else:
        return link


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
