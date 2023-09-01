"""
These commands are functions that ChatGPT will use 
if the user requests it. 

So far the user can ask ChatGPT to:
- Open or close an application
- Interact with their spotify by:
    - Playing an album, playlist, or song.
"""

# ************************************************
# * Utilities
import AppOpener
from dotenv import load_dotenv
import psutil

import traceback

from spotify_player import Spotify_Player



load_dotenv('.env')

# ************************************************


# * Utility functions
def is_open(app_name: str, include_exe: bool = False) -> bool:
    """
    Confirms if an application is open or not.
    
    Parameters:
    - include_exe : bool (optional)
        - Determines if .exe should be included in the application 
          name to search for.
    Returns:

    """

    if include_exe:
        app_name = str.strip(app_name) + ".exe"


    opened = False
    for i in psutil.process_iter():
        if str.lower(app_name) in str.lower(i.name()):
            opened = True
            break
    
    return opened

# *********************************
# * Commands

# * Open an app
def open_app(name: str) -> str:
    """
    Uses the AppOpener python package to open an application

    Parameters:
    - name : str
        - The name of the application
    """


    # * First check if the app is already opened
    # for i in psutil.process_iter():
    #     if str.lower(name) in str.lower(i.name()):
    #         print(i.name())
    #         not_opened = False
            
    # opened = is_open(name)

    # if not opened:
    try:
        print("Attempting to open app")
        AppOpener.open(name, match_closest=True, throw_error=True, output=False)
    except:
        error = traceback.format_exc
        traceback.print_exc()
        return error
    else:
        output = format("{name} was successfully opened")
        return output

# * Close an app
def close_app(name: str) -> str:
    """
    Uses the AppOpener python package to close an application

    Parameters:
    - name : str
        - The name of the application
    """

    try:
        AppOpener.close(name, match_closest=True, throw_error=True, output=False)
    except:
        traceback.print_exc()
    else:
        output = format("{name} was successfully closed".format(name=name))
        return output


# * Commands that will use the Spotify_Player class

def use_spotify_player(spotify_object: type[Spotify_Player], play_option: bool = True, item: str = "", type: str="track"):

    """
    Uses an instance of the Spotify_Player class to play music on Spotify.

    Parameters:
    - spotify_object : type[Spotify_Player]
        - An instance of the Spotify_Player class
    - play_option : bool, optional
        - Determines whether to play or pause the user's music on spotify.
        True --> play, False --> pause
    - item : str, optional
        - The item that the user wants to play on Spotify.
    - type : str
        - The type of the item the user wants to play.
        Options --> "Track", "Album", "Playlist"
    """


    # * Determine if the user wants to play or pause the playback on Spotify
    if play_option:

        # * Determine if type is track, album, or playlist
        if "track" in type.lower():

            spotify_object.play_track(item)
        
        elif "album" in type.lower():

            spotify_object.play_album(item)

        elif "playlist" in type.lower():

            spotify_object.play_playlist(item)
    
    else:
        spotify_object.pause()
    
    return "success"


def sleep() -> None:
    """
    This function will be passed to ChatGPT. This function will help
    determine if user input should continue to be processed or not.
    """
    return ""
