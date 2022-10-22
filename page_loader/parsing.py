import os
import requests as req
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from page_loader.naming_generators import generate_assets_path
import logging
from progress.bar import Bar
from page_loader.naming_generators import url2name


def makedir(output, dirname):
    newpath = f'{os.path.join(os.getcwd(), output, dirname)}'
    if not os.path.exists(newpath):  # Check if dir already exists
        logging.info(
            f"Directory not exists: {newpath}")
        os.makedirs(newpath)
    return newpath


def download_assets(for_down, output):
    bar = Bar('Loading', fill='|', suffix='%(percent)d%%', max=len(for_down))
    for asset in for_down:
        bar.next()
        filename, link = asset[0], asset[1]  # Get info from array
        out = os.path.join(output, filename)  # Create right output path
        try:
            r = req.get(link)
            with open(out, 'wb') as f:
                f.write(r.content)
        except Exception as ex:
            cause_info = (ex.__class__, ex, ex.__traceback__)
            logging.debug(str(ex), exc_info=cause_info)
            logging.warning(f"Resource {link} wasn't downloaded")
    bar.finish()


def validator_assets(url, link):
    down_link = link[:]  # Copy link
    if not down_link.startswith('https://') or 'http://':
        down_link = urljoin(url, link)  # Create download link
    if urlparse(down_link).netloc == urlparse(url).netloc:  # If link is local
        filename = link.split('/')[-1]  # Extract filename from link
        rename_index = down_link.rfind('/')
        rename_link = url2name(down_link[:rename_index].strip('/'))
        filename = f"{rename_link}-{filename}"  # Rename filename by full path
        filename = filename if '.' in filename \
            else f"{url2name(down_link)}.html"  # Has no extention - it's HTML
        if '?' in filename:  # Check for GET request in filename
            index = filename.rfind('?')
            filename = filename[:index]
        return filename, down_link  # Successful return of local link and name
    return '0', down_link  # Return non-local as zero


def prepare_assets(url, site_name):
    response = req.get(url)  # Get response
    if response.status_code != 200:  # Check if resp is success
        raise Warning(f'Status code error: {response.status_code}')
    for_download = []  # Array with assets info as name and link
    soup = bs(response.content, 'html.parser')
    assets = ['img', 'link', 'script']  # List of assets we need
    for asset in assets:
        attr = 'src' if asset in ('img', 'script') else 'href'  # Get right attr
        for link in soup.find_all(asset):
            if link.attrs.get(attr):  # If link has src or href attr
                filename, down_link = validator_assets(url, link[attr])
                if filename == '0':  # Check validated info for non-local links
                    continue
                for_download.append((filename, down_link))
                # Generate new paths for HTML file
                new_link_name = generate_assets_path(link[attr], site_name, url)
                # Replace paths with newly generated
                link[attr] = link[attr].replace(link[attr], new_link_name)
    return soup.prettify(), for_download
