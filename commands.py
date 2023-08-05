
# ************************************************
# * Packages to be used to assist with the commands.

from AppOpener import open, close
import spotipy
import os


# ************************************************

# * Open an app
def open_app(name: str) -> str:

    try:
        print("Attempting to open app")
        open(name, match_closest=True, throw_error=True, output=False)
    except Exception as e:
        print(e)
    else:
        output = format("Opening {name}")
        return output

# * Close an app
def close_app(name: str) -> str:

    try:
        close(name, match_closest=True, throw_error=True, output=False)
    except Exception as e:
        print(e)
    else:
        output = format("Closing {name}")
        return output
    
# * Play a song on spotify

class Spotify_Player:
    
    def __init__(self):
        """
        
        """
        # * Whats needed?
        # * - username
        # * - client id, client secret, and redirect uri
        self.SPOTIFY_CLIENT_ID: str = os.getenv('SPOTIFY_CLIENT_ID')
    
    def play():
        """
        
        """
    
    def pause():
        """
        
        """

    def play_song():
        """
        
        """
    
    def play_playlist():
        """
        
        """
    
    def play_album():
        """
        
        """