import os
import logging
from page_loader.parsing import prepare_assets, download_assets
from page_loader.url import url2name


def download(url, output):
    logging.basicConfig(level='INFO')
    logger = logging.getLogger()
    logger.info(f'Requested url: {url}')
    site_name = url2name(url)  # Get the right name for file
    html_out = os.path.join(output, f"{site_name}.html")
    logger.info(f'Writing file to: {html_out}')
    html, for_down = prepare_assets(url, site_name)
    with open(html_out, 'w', encoding='UTF-8') as f:
        f.write(html)
    logger.info('Downloading assets..')

    output_files = f'{os.path.join(os.getcwd(), output, f"{site_name}_files")}'
    if not os.path.exists(output_files):  # Check if dir already exists
        logging.info(
            f"Directory not exists: {output_files}")
        os.makedirs(output_files)

    download_assets(for_down, output_files)
    logger.info('Finished!')
    return html_out
