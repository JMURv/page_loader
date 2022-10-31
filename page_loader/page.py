import os
import logging
from page_loader.assets import prepare_assets, download_assets
from page_loader.url import url2name


def download(url, output_dir):
    logging.info(f'Requested url: {url}')
    site_name = url2name(url)  # Get the right name for file
    html_outpath = os.path.join(output_dir, f"{site_name}.html")
    logging.info(f'Writing file to: {html_outpath}')
    html, media_files = prepare_assets(url, output_dir)
    with open(html_outpath, 'w', encoding='UTF-8') as f:
        f.write(html)
    download_assets(media_files, output_dir, url)
    logging.info('Finished!')
    return html_outpath
