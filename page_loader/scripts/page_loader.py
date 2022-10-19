from page_loader.cli import get_arguments
from page_loader import download


def main():
    arg = get_arguments()
    path = download(arg.url, arg.output)
    print(f"{arg.url} was saved here: {path}")


if __name__ == '__main__':
    main()
