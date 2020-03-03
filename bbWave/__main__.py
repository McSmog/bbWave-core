import sys
import argparse
import logging

import bbWave.config as config
import bbWave.files.metadata as metadata
from bbWave.files.treewalker import TreeWalker
from bbWave.database import Database

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

    db = Database(CONFIG['DATABASE']['path'])

    tree_walker = TreeWalker(CONFIG['PATH']['music_directory'])
    tree_walker.build_files_list()

    logging.info('Found {} files'.format(tree_walker.files_count))

    meta_to_db = []
    processed = 0
    for filepath in tree_walker.get_file_list():
        new_meta = metadata.get_audio_info(filepath)
        if new_meta:
            meta_to_db.append(new_meta)
            processed += 1

    logging.info('Successfully processed {} of {} ({} errors)'.format(processed, tree_walker.files_count,
                                                                      tree_walker.files_count - processed))

    db.record_music_info(meta_to_db)


if __name__ == '__main__':
    main()
