import os
import logging
from page_loader.parsing import makedir, prepare_assets, download_assets
from page_loader.naming_generators import url2name


def download(url, output):
    logging.basicConfig(level='INFO')
    logger = logging.getLogger()
    logger.info(f'Requested url: {url}')
    site_name = url2name(url)
    html_out = os.path.join(output, f"{site_name}.html")
    logger.info(f'Writing file to: {html_out}')
    html, for_down = prepare_assets(url, site_name)
    with open(html_out, 'w', encoding='UTF-8') as f:
        f.write(html)
    logger.info('Downloading assets..')
    output_files = makedir(output, f"{site_name}_files")
    download_assets(for_down, output_files)
    logger.info('Finished!')
    return html_out
