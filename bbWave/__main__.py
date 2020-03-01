import sys
import logging

import bbWave.files.metadata as metadata
from bbWave.files.treewalker import TreeWalker


def main():
    tree_walker = TreeWalker(str(sys.argv[1]))
    tree_walker.build_files_list()

    for filepath in tree_walker.get_file_list():
        print(metadata.get_audio_info(filepath))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} <path>'.format(sys.argv[0]))
        sys.exit(-1)

    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.DEBUG)

    main()
