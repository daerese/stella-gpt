import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth


import sys
import json
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

from colorama import Fore, Back, Style

import requests


from dotenv import load_dotenv
import os

# ************************

"""
PLAYING MUSIC:
The user will have the option to play the following:
- Album (type=album)
- Song (type=track)
- Artist (type=artist)
- Playlist (type=playlist)
---- type is specified in the search query


About playing playlists, How can we get the playlists that the user follows?

"""

# *************************

load_dotenv(".env")

# * Use the following to print out json data in readable format
def print_json(var):
    print(json.dumps(var, sort_keys=True, indent=4))


# example_playlist_uri -> "spotify:playlist:71LlA9AbMCOwMBWQe0kaWS"
# leave the door open -> "spotify:track:02VBYrHfVwfEWXk5DXyf0T"

# *************************

# * Test code
# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
# spotify = spotipy.Spotify(
#     client_credentials_manager=SpotifyClientCredentials(
#         # client_id=os.getenv('SPOTIPY_CLIENT_ID'),
#         # client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
#     )
#     )

# results = spotify.artist_albums(birdy_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])

# for album in albums:
#     print(album['name'])

# *************************
# * My code

# try:
#     token = util.prompt_for_user_token(user_id)
# except:
#     os.remove(f".cache-{user_id}")
#     token = util.prompt_for_user_token(user_id)

# * Utility function to return the authorization header for requests
def get_auth_header(token):
    return {"Authorization": "Bearer "+ token}


def search_for_playlist(token: str, playlist: str) -> json:
    """
    Return the playlist searched for by the user.
    """

    # * In order the playlist a user searches for, we have to make 
    # * our own request to the Spotify API.
    # * The reason is that the results return the playlists owned/followed
    # * by the user at the top. 
    # * However, the python Spotipy library does not.
    #  
    url = "https://api.spotify.com/v1/search"

    url_query = "?q={playlist}&type=playlist&limit=3".format(playlist=playlist)

    header = get_auth_header(token)

    response = requests.get(
        url=url + url_query,
        headers=header
    )

    return response.json()


# Create spotify object
spotifyObject = spotipy.Spotify(
    # auth=token,
    auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=[
            "streaming", 
            "user-modify-playback-state", 
            "user-read-playback-state",
            "playlist-read-private"
        ],
    )
)

user = spotifyObject.current_user()

file = open('.cache')

data = json.load(file)

token = data["access_token"]

while True:
    print()
    print(">>> Welcome to Spotify " + user['display_name'])
    print(">>> You have " + str(user['followers']['total']) + " Followers")
    print()
    print("0 - Play a song on Spotify")
    print("1 - Play a playlist on Spotify")
    print("2 - Play an album on Spotify")
    print("3 - Get your available devices")
    print("4 - exit")
    choice = int(input("Your choice: "))

    if choice < 4:

        # * Play a track
        if choice == 0:
            print()
            searchQuery = input("Ok, What song would you like to play: ")
            print()

            searchResults = spotifyObject.search(q=searchQuery, type="track", limit=1)

            # Play the song
            track = searchResults["tracks"]["items"][0]["uri"]
            track_name = searchResults["tracks"]["items"][0]["name"]

            spotifyObject.start_playback(
                device_id=os.getenv("DESKTOP_SPOTIFY_ID"),
                uris=[track]
            )


            print(Fore.CYAN)
            print("Playing {track_name}".format(track_name=track_name))

            print("\nTrack URI: {track}".format(track=track))
            print(Style.RESET_ALL)
        
        elif choice == 1:
            print()
            searchQuery = input("Ok, What playlist would you like to play: ")
            print()

            # * Search through the user's owned/followed playlists

            results = search_for_playlist(token=token, playlist=searchQuery)

            playlist = results["playlists"]["items"][0]

            # * Start the playback of the playlist
            spotifyObject.start_playback(
                device_id=os.getenv("DESKTOP_SPOTIFY_ID"),
                context_uri=playlist["uri"]
            )

            print(Fore.CYAN)
            print("Playing {playlist}".format(playlist=playlist["name"]))
            print(Style.RESET_ALL)

        elif choice == 3:

            devices = spotifyObject.devices()["devices"]

            print_json(devices)





    if choice == 4:
        break

# *************************
