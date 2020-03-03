import logging
import mutagen


def get_basic_info(raw_meta, no_tags=False):
    info = {
        'file_path': raw_meta.filename,
        'length': int(raw_meta.info.length),
        'title': '',
        'artist': '',
        'album': '',
        'genre': '',
        'track_number': '',
        'year': ''
    }

    if no_tags:
        # Get file name
        title_raw = raw_meta.filename.split('/')[-1]

        # Remove extension
        title = title_raw.split('.')
        title.pop()
        info['title'] = ''.join(title)

    return info


def get_tag_info(raw_meta):
    """Filling empty tags for DB"""

    # Check if it is a *.mp3 file
    its_mp3 = False
    for mime in raw_meta.mime:
        if mime == 'audio/mp3':
            its_mp3 = True

    if its_mp3:
        tags = {
            'title': raw_meta.tags.get(['TALB'][0], ''),
            'artist': raw_meta.tags.get(['TPE1'][0], ''),
            'album': raw_meta.tags.get(['TALB'][0], ''),
            'genre': raw_meta.tags.get(['TCON'][0], ''),
            'track_number': raw_meta.tags.get(['TRCK'][0], ''),
            'year': raw_meta.tags.get(['TDRC'][0], '')
        }
    else:
        tags = {
            'title': raw_meta.tags.get(['TITLE'][0], ''),
            'artist': raw_meta.tags.get(['ARTIST'][0], ''),
            'album': raw_meta.tags.get(['ALBUM'][0], ''),
            'genre': raw_meta.tags.get(['GENRE'][0], ''),
            'track_number': raw_meta.tags.get(['TRACKNUMBER'][0], ''),
            'year': raw_meta.tags.get(['DATE'][0], '')
        }

    for key, value in tags.items():
        tags[key] = value[0] if type(tags[key]) is list else str(value)

    # Removing slashes and leading zeroes
    if tags['track_number'] != '':
        try:
            tags['track_number'] = int(tags['track_number'].split('/')[0])
        except ValueError:
            tags['track_number'] = ''

    return {
        **get_basic_info(raw_meta),
        **tags
    }


def get_audio_info(path_to_file):
    try:
        raw_meta = mutagen.File(path_to_file)
    except mutagen.MutagenError:
        logging.error('Corrupted metadata on "{}"'.format(path_to_file))
        return None

    # Got some weird shit
    if raw_meta is None:
        logging.error('Cannot parse metadata on "{}"'.format(path_to_file))
        return None

    # Audio file has tags
    if raw_meta:
        return get_tag_info(raw_meta)
    # Audio file just identified by mutagen
    else:
        a = get_basic_info(raw_meta, no_tags=True)
        return a
