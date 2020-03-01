import argparse
import logging

import bbWave.config as config
import bbWave.files.metadata as metadata
from bbWave.files.treewalker import TreeWalker

CONFIG = []


def parse_arguments():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-c', '--config', help='path to configuration file')

    return parser.parse_args()


def main():
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.DEBUG)

    args = parse_arguments()

    global CONFIG
    CONFIG = config.get_configuration(args.config)
    print(CONFIG)

    tree_walker = TreeWalker(CONFIG['PATH']['music_directory'])
    tree_walker.build_files_list()

    meta_to_db = []
    for filepath in tree_walker.get_file_list():
        meta_to_db.append(metadata.get_audio_info(filepath))
    print(len(meta_to_db))


if __name__ == '__main__':
    main()
