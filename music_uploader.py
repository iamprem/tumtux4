import os
import glob
from gmusicapi import Musicmanager
from gmusicapi import Mobileclient
from oauth2client.file import Storage


SONGS_DIR = 'songs/'
MUSIC_OAUTH_FILE = 'music_credentials.json'
GPLAY_MOBILE_CLIENT = 'mobileclient.json'


def get_music_manager():
    music_manager = Musicmanager(debug_logging=True)
    if not music_manager.login(oauth_credentials=MUSIC_OAUTH_FILE):
        print('Not able to login with existing credentials, performing oauth flow')
        music_manager.perform_oauth(storage_filepath=MUSIC_OAUTH_FILE)
    return music_manager


def delete_songs():
    mc = Mobileclient()
    if not mc.oauth_login(oauth_credentials=GPLAY_MOBILE_CLIENT, device_id=Mobileclient.FROM_MAC_ADDRESS):
        print('Not able to login with existing credentials, performing oauth flow')
        mc.perform_oauth(storage_filepath=GPLAY_MOBILE_CLIENT)
    songs = mc.get_all_songs()
    for song in songs:
        mc.delete_songs(song.get('id'))


if __name__ == "__main__":
    music_manager = get_music_manager()
    file_paths = []
    for filename in glob.glob(os.path.join(SONGS_DIR, '*.mp3')):
        uploads = music_manager.upload(filename, enable_matching=True)
        print(uploads)
