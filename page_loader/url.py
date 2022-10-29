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
    filename = f"{url2name(path)}{extension}"  # Rename filename by full path
    if '.' not in filename:
        filename = f"{filename}.html"
    if '?' in filename:  # Check for GET request in filename
        filename = filename[:filename.rfind('?')]
    return filename


def generate_html_path(or_url, url):
    path, extension = os.path.splitext(url)
    if '.' in extension:
        return f"{to_dir_path(or_url)}{create_filename(url)}"
    return f"{to_dir_path(or_url)}{create_filename(url)}"
