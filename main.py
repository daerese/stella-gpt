
import elevenlabs as eleven
import openai
import json

import inspect


from conversation import Conversation
from listener import *

from dotenv import load_dotenv
import os

from commands import *
from spotify_player import Spotify_Player   

import eel

# *******************************

# * Environment variables
load_dotenv('.env')

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

ELEVEN_API_KEY: str = os.getenv("ELEVEN_API_KEY")

VOICE_ID: str = os.getenv("VOICE_ID")

# * Spotify Environment variables


# * API Keys
openai.api_key = OPENAI_API_KEY
# eleven.set_api_key(ELEVEN_API_KEY)


# *******************************
# * Utility functions
def extract_args(args: dict) -> list:
    """
    Extracts the arguments from ChatGPT's response when
    it wants to call a function.
    """
    args_to_call = []
    for arg in args:
        args_to_call.append(args.get(arg))
    
    return args_to_call



# *******************************


def get_voices():
    pass
    # return eleven.voices()


def get_character_info(character_name, omit_age):

    """
    returns the the requested character information in JSON format
    """

    characters = {
        "amy": {
            "role": "support character",
            "age": "36",
            "power": "Flower petals / Teleportation"
        },
        "jessica": {
            "role": "Antagonist",
            "age": "34",
            "power": "Chaos / Time manipulation"
        }
    }

    return json.dumps(characters[character_name])
    

# * Commands
commands = [
    {
        "name": "get_character_info",
        "description": "Get the information of one of the characters from the story Starflower",
        "parameters": {
            "type": "object",
            "properties": {
                "character_name": {
                    "type": "string",
                    "description": "The name of the character requested",
                    "enum": ["jessica", "amy"]
                },
                "omit_age": {
                    "type": "boolean",
                    "description": "Gives the option to leave out the age of the character"
                },
            },
            "required": ["character_name", "omit_age"],
        },
    },
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
        "description": "If the user doesn't need any more assistance at the moment\
                        This function should be called. You will take no more input from the user until they request\
                        your assistance again",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]

# available_functions = {
#                         "get_character_info": get_character_info
#                     }

available_commands = {}

for command in commands:

    # * eval() converts a string type into a function
    command_name = command["name"]
    available_commands[command_name] = eval(command_name)

# * A test function that will be called from Javascript (script.js)
@eel.expose
def py_print(message="the string was not passed :("):
    # print(message)
    print(message)

@eel.expose
def call_from_py():
    eel.log_on_js()


@eel.expose
def start():
    
    print("Finding microphone...")

    # * Getting the Caroline voice
    # voices = get_voices()

    # caroline = list(filter(lambda voice: voice.voice_id == VOICE_ID, voices))[0]

    # * ChatGPT Prompt configuration
    prompt = """Your name is Stella. You are my friendly assistant. You often like to be sarcastic, and make occasional jokes.
                You are connected to an application on my computer. I'm using my voice to communicate with you, and turning my speech into text via a speech recognition software.
                I may ask for a task related to taking an action on my computer, such as opening an application, or sending an email.
                Do not deny the request or say that you can't do it unless it's absolutely impossible.
                You also have the ability to play something on Spotify on the user's computer if you are asked.
                When you receive the awake command from the user: "hey stella", return a short and breif message letting them know 
                that you're listening
                """

    conversation = Conversation(prompt)


    
    while True:

        # * 1. Listen for user input
        # * 2. Wait for the wake word: "Stella" or "Hey Stella"
        # * 3. After the wake word is heard, the program will
        # *    listen for inputs to send to ChatGPT

        awake = False



        user_input: dict = listen()

        input_message: str = user_input["message"]

        input_error: bool = user_input["error"]

    
        if not input_error and "hey stella" in input_message:

            awake = True

            print("Awoken")

            while awake:

                role = "user" if not input_error else "system"
                
                conversation.add_message(role=role, content=input_message)

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=conversation.get_messages(),

                    functions=commands,
                    function_call="auto",

                    temperature=1.25,
                    # max_tokens=75,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
            
                
                try:

                    # ************************************
                    # * Append ChatGPT response to have context in the current conversation.
                    message = response["choices"][0]["message"]
                    # print(message)
                    # * Function calling
                    if message.get("function_call"):

                        # * Extract the information about the function that 
                        # * ChatGPT wants to be called.
                        function_name = message["function_call"]["name"]
                        arguments = json.loads(message["function_call"]["arguments"])

                        function_to_call = available_commands[function_name]

                        # * Call the function, using the arguments. 
                        # * Also, determine if the use_spotify_player function is being called

                        if function_name == "use_spotify_player":

                            # * Create a spotify object if it isn't already created.
                            if "spotify_object" not in locals():
                                spotify_object = Spotify_Player()

                            function_response = function_to_call(spotify_object, *extract_args(arguments))
                        
                        elif function_name == "sleep":
                            result = function_to_call()
                            awake = result["result"]
                            function_response = result["message"]
                        else:
                            function_response = function_to_call(*extract_args(arguments))

                        conversation.add_message(role="function", 
                                                content=function_response,
                                                function_name=function_name,
                                                )
                        
                        # * Generate another response based on the called function
                        second_response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=conversation.get_messages(),

                            temperature=1.25,
                            max_tokens=75,
                            top_p=1,
                            frequency_penalty=0,
                            presence_penalty=0
                        )
                        
                        message = second_response["choices"][0]["message"]
                    # ************************************
                except Exception as error:
                    print("There was an error: \n", error)
                else:
                    conversation.add_message(content=message["content"], role="assistant")

                    # * Generate the voice using a message.
                    # audio = eleven.generate(
                    #     text=message["content"],
                    #     voice=caroline,
                    #     model="eleven_multilingual_v1"
                    # )

                print("\nPlaying audio...")
                

                print(message["content"])
                generate_audio(message["content"])

                # * Call the function from JavaScript to play the audio 
                # * on the frontend.
                eel.playAudio()
                # eleven.play(audio, use_ffmpeg=False)

                # * Take another input and reset
                user_input = listen()

                input_message = user_input["message"]

                input_error = user_input["error"]



        else:
            print("Try again")


def main():
    eel.init('gui')

    eel.start('main.html')

if __name__ == '__main__':
    main()