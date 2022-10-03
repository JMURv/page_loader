from page_loader.cli import get_arguments
from page_loader import download


def main():
    arguments = get_arguments()
    print(
        download(
            arguments.url,
            arguments.output_path
        )
    )


if __name__ == '__main__':
    main()
