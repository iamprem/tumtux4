import os
import glob
from gmusicapi import Musicmanager
from gmusicapi import Mobileclient
from oauth2client.file import Storage
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

SONGS_DIR = 'songs/'
MUSIC_OAUTH_FILE = 'music_credentials.json'
GPLAY_MOBILE_CLIENT = 'mobileclient.json'


def get_music_manager():
    music_manager = Musicmanager(debug_logging=True)
    if not music_manager.login(oauth_credentials=MUSIC_OAUTH_FILE):
        print('Not able to login with existing credentials, performing oauth flow')
        music_manager.perform_oauth(storage_filepath=MUSIC_OAUTH_FILE)
    return music_manager


def merge_album_art(filename):
    audio = MP3(filename, ID3=ID3)
    audio.tags.add(
        APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc=u'Cover',
            data=open(filename[:-4] + '.jpg', 'rb').read()
        )
    )
    audio.save()


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
        #    merge_album_art(filename)
        uploads = music_manager.upload(filename, enable_matching=True)
        print(uploads)
        os.remove(filename)
