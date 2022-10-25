from urllib.parse import urljoin, urlparse
import re


def url2name(url):
    parsed = urlparse(url.strip('/'))
    url = f"{parsed.netloc}{parsed.path}"
    reg_exp = re.compile(r"[^a-zA-Z\d+]")
    result = reg_exp.sub('-', url)
    return result


def local_path(url, link):
    filename = link.split('/')[-1]
    new_url = urljoin(url, link)
    name_index = new_url.rfind('/')
    site_name = url2name(url)
    if '.' in filename:
        return f"{site_name}_files/{url2name(new_url[:name_index])}-{filename}"
    return f"{site_name}_files/{url2name(new_url[:name_index])}-{filename}.html"


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
