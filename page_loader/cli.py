import argparse
import os


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Download HTML pages!'
    )
    parser.add_argument(
        "-o", '--output', help="set output path", default=os.getcwd()
    )
    parser.add_argument("url")
    # parser.add_argument("output_path")
    return parser.parse_args()
