from urllib.parse import urlparse
import re
import os


def url2name(url):
    parsed = urlparse(url.strip('/'))
    url = f"{parsed.netloc}{parsed.path}"
    reg_exp = re.compile(r"[^a-zA-Z\d+]")
    result = reg_exp.sub('-', url)
    return result


def to_dir_path(url):
    return f"{url2name(url)}_files/"


def generate_path(url, path_to_asset):
    path, extension = os.path.splitext(path_to_asset)
    filename = f"{url2name(path)}{extension}"
    if '.' not in extension:
        filename = f"{filename}.html"
    if '?' in filename:
        filename = filename[:filename.rfind('?')]
    return f"{to_dir_path(url)}{filename}"
