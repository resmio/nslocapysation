__author__ = 'JanNash'

import argparse
import logging
import os
from nslocapysation.tools import (
    collect_m_and_lproj_file_paths
)


__version__ = "0.1"
__license__ = "MIT"

USAGE = "%prog [options] <url>"
VERSION = "%prog v" + __version__


def parse_args():
    """
    Parses command-line arguments and returns the parsed namespace-object.
    """
    parser = argparse.ArgumentParser(usage=USAGE, version=VERSION)

    parser.add_argument(
        "-d", "--debug",
        action="store_true", default=False, dest="debug",
        help="Set logging level to DEBUG. Beware, it's gonna be verbose :)."
    )

    parser.add_argument(
        "-p", "--path",
        action="store", type=str, default=os.getcwd(), dest="project_source_root_path",
        help=("The path to the Xcode-project's source-root folder that will be walked. "
              "Defaults to the current working directory.")
    )

    return parser.parse_args()

def run(project_source_root_path):
    file_paths = collect_m_and_lproj_file_paths(project_source_root_path)

    pass


if __name__ == '__main__':
    args = parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    run(project_source_root_path=args.project_source_root_path)