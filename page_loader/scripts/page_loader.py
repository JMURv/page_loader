import sys
import logging
from page_loader.cli import get_arguments
from page_loader import download


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        arg = get_arguments()
        path = download(arg.url, arg.output)
        print(f"{arg.url} was saved here: {path}")
    except Exception as ex:
        logging.error(ex)
        sys.exit(0)


if __name__ == '__main__':
    main()
