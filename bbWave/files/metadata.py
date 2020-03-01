import mutagen


def get_audio_info(path_to_file):
    return mutagen.File(path_to_file)
