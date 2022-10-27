import os
import logging
from page_loader.assets import prepare_assets, download_assets
from page_loader.url import url2name


def download(url, output):
    logger = logging.getLogger()
    logger.info(f'Requested url: {url}')
    site_name = url2name(url)  # Get the right name for file
    html_outpath = os.path.join(output, f"{site_name}.html")
    logger.info(f'Writing file to: {html_outpath}')
    html, for_down = prepare_assets(url)
    with open(html_outpath, 'w', encoding='UTF-8') as f:
        f.write(html)
    logger.info('Downloading assets..')
    output_files = f'{os.path.join(os.getcwd(), output, f"{site_name}_files")}'
    download_assets(for_down, output_files)
    logger.info('Finished!')
    return html_outpath
