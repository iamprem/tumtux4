# -*- coding: utf-8 -*-
from google.oauth2.credentials import Credentials
import googleapiclient.errors
import googleapiclient.discovery
import google_auth_oauthlib.flow
from pytube import YouTube
import youtube_dl
import json
import os

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
CLIENT_SECRETS_FILE = "client_secret.json"
YOUTUBE_CHANNEL_ID = "UCERyYfZvwoWkf66MexKxznw"
YOUTUBE_USER_ID = "ERyYfZvwoWkf66MexKxznw"
YOUTUBE_URL = "https://www.youtube.com/watch?v="
YDL_OPTS = {
    'format': 'bestaudio/best',
    'outtmpl': 'songs/%(title)s.%(ext)s',
    'download_archive': 'archive.txt',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
# Disable OAuthlib's HTTPS verification when running locally.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


def get_credentials():
    if os.path.isfile("credentials.json"):
        with open("credentials.json", 'r') as f:
            creds_data = json.load(f)
        creds = Credentials(
            None,
            refresh_token=creds_data['refresh_token'],
            token_uri=creds_data['token_uri'],
            client_id=creds_data['client_id'],
            client_secret=creds_data['client_secret']
        )
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
        creds = flow.run_console()
        creds_data = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }
        with open("credentials.json", 'w') as outfile:
            json.dump(creds_data, outfile)
    return creds


def get_playlists(youtube):
    request = youtube.playlists().list(
        part="id,snippet,contentDetails",
        maxResults=50,
        mine=True
    )
    response = request.execute()
    return response['items']


def filter_music_playlists(playlists):
    music_playlists = {}
    for playlist in playlists:
        playlist_name = playlist['snippet']['title']
        if playlist_name.startswith('Music - '):
            music_playlists[playlist_name] = playlist['id']
    return music_playlists


def get_playlist_items(youtube, playlistId):
    nextPageToken = None
    playlist_items = []

    while True:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=playlistId,
            pageToken=nextPageToken
        )
        response = request.execute()
        playlist_items.extend(response['items'])
        nextPageToken = response.get('nextPageToken')
        if nextPageToken is None:
            break
    return playlist_items


def download_yt_audio(videoId):
    """
    https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
    """
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        ydl.download([YOUTUBE_URL + videoId])


def main():
    api_service_name = "youtube"
    api_version = "v3"
    credentials = get_credentials()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    playlists = get_playlists(youtube)
    # print(json.dumps(playlists, indent=4, sort_keys=True))
    music_playlists = filter_music_playlists(playlists)
    for _, playlistId in music_playlists.items():
        playlist_items = get_playlist_items(youtube, playlistId)
        for video in playlist_items:
            print(json.dumps(video, indent=4))
            download_yt_audio(video['snippet']['resourceId']['videoId'])


if __name__ == "__main__":
    main()
