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


def create_filename(url):
    path, extension = os.path.splitext(url)
    filename = f"{url2name(path)}{extension}"
    if '.' not in filename:
        filename = f"{filename}.html"
    if '?' in filename:
        filename = filename[:filename.rfind('?')]
    return filename


def generate_html_path(url, path_to_asset):
    path, extension = os.path.splitext(path_to_asset)
    if '.' in extension:
        return f"{to_dir_path(url)}{create_filename(path_to_asset)}"
    return f"{to_dir_path(url)}{create_filename(path_to_asset)}"
