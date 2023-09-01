"""
In order for ChatGPT to use our functions, they need 
they need to be described in a the format Dict[str, str]. If you have 
a custom function, write the details of your function in 
a new dictionary object in the commands array.

For more details, you can read the ChatGPT official documentation here:
https://platform.openai.com/docs/guides/gpt/function-calling
"""

commands = [
    {
        "name": "open_app",
        "description": "Start an application on the user's computer if asked to, \
                        If the application is already opened, inform the user of that.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the application"
                },
            },
            "required": ["name"]
        }
    },
    {
        "name": "close_app",
        "description": "Close an application on the user's computer if asked to. \
                        If the application is already closed, inform the user of that",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the application"
                },
            },
            "required": ["name"]
        }
    },
    {
        "name": "use_spotify_player",
        "description": "Uses an instance of the Spotify_Player class to play music on Spotify.",
        "parameters": {
            "type": "object",
            "properties": {
                "play_option": {
                    "type": "boolean",
                    "description": "Determines whether the user pause or play something on Spotify\
                                    If the user wants to pause their music, or resume the current playback, then no other parameter is required\
                                    True to play, False to pause"
                },
                "item": {
                    "type": "string",
                    "description": "The track that the user wants to play on Spotify."
                },
                "type": {
                    "type": "string",
                    "description": "The type of the item that the user wants to play",
                    "enum": ["track", "album", "playlist"]
                }
            },
            "required": ["play_option"]
        }
    },
    {
        "name": "sleep",
        "description": "If the user doesn't need any more assistance at the moment,\
                        or if you presume they are finished speaking to you for now, \
                        then this function should be called. You will take no more input until the user \
                        says the wake command 'hey stella' and requests more assistance.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]