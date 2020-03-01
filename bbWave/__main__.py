import logging

import bbWave.config as config
import bbWave.files.metadata as metadata
from bbWave.files.treewalker import TreeWalker

CONFIG = []


def main():
    global CONFIG
    CONFIG = config.get_configuration()
    print(CONFIG)

    tree_walker = TreeWalker(CONFIG['PATH']['music_directory'])
    tree_walker.build_files_list()

    for filepath in tree_walker.get_file_list():
        print(metadata.get_audio_info(filepath))


if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.DEBUG)

    main()
