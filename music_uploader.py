import os
import glob
from gmusicapi import Musicmanager
from oauth2client.file import Storage


SONGS_DIR = 'songs/'


def get_music_manager():
    music_manager = Musicmanager(debug_logging=True)
    if not music_manager.login("music_credentials.json"):
        music_manager.perform_oauth(storage_filepath="music_credentials.json")
    return music_manager


def upload():
    pass


if __name__ == "__main__":
    music_manager = get_music_manager()
    file_paths = []
    for filename in glob.glob(os.path.join(SONGS_DIR, '*.mp3')):
        file_paths.append(filename)
    uploads = music_manager.upload(file_paths, enable_matching=True)
    print(uploads)
