# Setup Guide

* Install the requirements.txt file using pip (preferrably in virtualenv)
* Install ffmpeg for audio format conversion
* Setup a google cloud project with access to Youtbe Data API. (Download the oauth ```client_secret.json``` file in project root directory)
* Run ```python main.py``` to start the application (Download from youtube).
  * First time this will get you through oauth workflow to grant the app permission to access your youtube account.
  * Above step will create a ```credentials.json``` file that will have the refresh token to be used for future authentication.
* Run ```python music_uploader.py``` to upload songs to Googe play music.
  * First time this will get you through oauth workflow similar to above to allow Google MusicManager to access your Google play music account,
  * Above step will create a ```music_credentials.json``` file that will have the refresh token to be used for future authentication.

## Reference links

* API Cosole: https://console.developers.google.com/

* Credentials: https://stackoverflow.com/questions/27771324/google-api-getting-credentials-from-refresh-token-with-oauth2client-client
