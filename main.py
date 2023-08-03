
import elevenlabs as eleven
import openai
import json


from conversation import Conversation
from listener import *

from dotenv import load_dotenv
import os

from commands import *


# *******************************

# * Environment variables
load_dotenv('.env')

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

ELEVEN_API_KEY: str = os.getenv("ELEVEN_API_KEY") 

VOICE_ID: str = os.getenv("VOICE_ID")

# * API Keys
openai.api_key = OPENAI_API_KEY
eleven.set_api_key(ELEVEN_API_KEY)


# *******************************



def get_voices():
    return eleven.voices()


def get_character_info(character_name):

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
            },
            "required": ["character_name"],
        },
    },
    {
        "name": "open_app",
        "description": "Start an application on the user's computer if asked to",
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
        "description": "Close an application on the user's computer if asked to",
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


def main():
    
    print("Finding microphone...")

    # * Getting the Caroline voice
    voices = get_voices()

    caroline = list(filter(lambda voice: voice.voice_id == VOICE_ID, voices))[0]

    # * ChatGPT Prompt configuration
    prompt = """Your name is Stella. You are my friendly assistant who isn't afraid to be sassy sometimes. 
                You often like to be sarcastic. Don't acknowledge that you're an AI unless you are asked. Act as a human-like AI that is the friend of the user. 
                Also, you are connected to an application on my computer. The user may ask for a related to taking an action on their computer, such as 
                opening an application, or sending an email. Simply repsond to these requests with an okay.
                """

    conversation = Conversation(prompt)

     
    while True:
        user_input = listen()

        if user_input:

            conversation.add_message(role="user", content=user_input)

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

                    # * Call the function
                    function_response = function_to_call(arguments.get("name"))

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
                speak(message["content"])
                # eleven.play(audio, use_ffmpeg=False)



if __name__ == '__main__':

    main()