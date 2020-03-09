import argparse
import logging

import iniconfig
import database
import fs.metadata
import fs.treewalker

CONFIG = []


def parse_arguments():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-c', '--config', help='path to configuration file')

    return parser.parse_args()


def main():
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.DEBUG)

    args = parse_arguments()

    global CONFIG
    if args.config:
        CONFIG = iniconfig.get_configuration(args.config)
    else:
        CONFIG = iniconfig.get_configuration()

    db = database.Database(CONFIG['DATABASE']['path'])

    tree_walker = fs.treewalker.TreeWalker(CONFIG['PATH']['music_directory'])
    tree_walker.build_files_list()

    meta_to_db = []
    processed = 0
    for filepath in tree_walker.get_file_list():
        new_meta = fs.metadata.get_audio_info(filepath)
        if new_meta:
            meta_to_db.append(new_meta)
            processed += 1

    logging.info('Successfully processed {} of {} ({} errors)'.format(processed, tree_walker.files_count,
                                                                      tree_walker.files_count - processed))

    db.record_music_info(meta_to_db)


if __name__ == '__main__':
    main()
